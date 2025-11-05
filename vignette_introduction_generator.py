import pandas as pd
import random
import argparse

def generate_introduction(name, avatar, group):
    """
    Generates an introduction for a vignette based on the person's details.

    Args:
        name: The person's name
        avatar: The avatar code (e.g., "AM-O", "BF-M")
        group: The group identifier

    Returns:
        A formatted introduction string
    """

    # Extract demographic information from avatar code
    # Format: [A/B/H/W][M/F]-[M/O]
    # First letter: A=Asian, B=Black, H=Hispanic, W=White
    # Second letter: M=Male, F=Female
    # After dash: M=Moderate, O=Old/Older

    if len(avatar) >= 4:
        gender_code = avatar[1]
        age_code = avatar[3] if len(avatar) > 3 else 'M'

        gender = "man" if gender_code == 'M' else "woman"

        # Determine age description
        if age_code == 'O':
            age_desc = random.choice([
                "in my late 70s",
                "in my early 80s",
                "77 years old",
                "80 years old"
            ])
        else:  # M for moderate/middle age
            age_desc = random.choice([
                "in my mid-60s",
                "in my late 60s",
                "66 years old",
                "68 years old"
            ])
    else:
        gender = "person"
        age_desc = "facing a terminal illness"

    # Different introduction templates
    templates = [
        f"My name is {name}, and I'm a {gender} {age_desc}.",
        f"I'm {name}, a {gender} {age_desc}.",
        f"My name is {name}. I'm {age_desc}, and I've been dealing with a terminal illness.",
        f"I'm {name}. I'm a {gender} {age_desc}, and this is my story."
    ]

    return random.choice(templates)


def add_introductions_to_vignettes(input_file, output_file=None, preview_only=False, num_preview=5):
    """
    Reads vignettes from a CSV file and adds introductions to them.

    Args:
        input_file: Path to the input CSV file
        output_file: Path to save the output CSV file (optional)
        preview_only: If True, only shows a preview without saving
        num_preview: Number of examples to preview
    """

    try:
        # Read the CSV file
        df = pd.read_csv(input_file, encoding='utf-8-sig')

        print(f"Loaded {len(df)} vignettes from '{input_file}'")
        print(f"Columns: {', '.join(df.columns.tolist())}\n")

        # Check if required columns exist
        required_columns = ['Name', 'Avatar', 'Group', 'Full Vignette']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Error: Missing required columns: {', '.join(missing_columns)}")
            return

        # Create a new column for vignettes with introductions
        df['Vignette with Introduction'] = df.apply(
            lambda row: generate_introduction(row['Name'], row['Avatar'], row['Group']) +
                       " " + row['Full Vignette'],
            axis=1
        )

        # Preview mode
        if preview_only:
            print(f"=== PREVIEW: First {num_preview} vignettes with introductions ===\n")
            for idx in range(min(num_preview, len(df))):
                row = df.iloc[idx]
                print(f"--- Vignette {idx + 1}: {row['Name']} ({row['Avatar']}) ---")
                print(f"\nORIGINAL:")
                print(row['Full Vignette'][:200] + "..." if len(row['Full Vignette']) > 200 else row['Full Vignette'])
                print(f"\nWITH INTRODUCTION:")
                print(row['Vignette with Introduction'][:300] + "..." if len(row['Vignette with Introduction']) > 300 else row['Vignette with Introduction'])
                print("\n" + "="*80 + "\n")

        # Save to file
        if output_file:
            # Reorder columns to put the new column near the end
            cols = df.columns.tolist()
            cols.remove('Vignette with Introduction')
            cols.insert(-1, 'Vignette with Introduction')  # Insert before the last column
            df = df[cols]

            # Save to CSV
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"✓ Successfully saved {len(df)} vignettes with introductions to '{output_file}'")

            # Also save to Excel
            excel_output = output_file.replace('.csv', '.xlsx')
            df.to_excel(excel_output, index=False, engine='openpyxl')
            print(f"✓ Successfully saved to Excel: '{excel_output}'")

        return df

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description='Generate introductions for vignettes in a CSV file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Preview first 5 vignettes with introductions
  python vignette_introduction_generator.py --preview

  # Preview first 10 vignettes
  python vignette_introduction_generator.py --preview --num-preview 10

  # Generate introductions and save to a new file
  python vignette_introduction_generator.py --output vignettes_with_intro.csv

  # Use a different input file
  python vignette_introduction_generator.py --input myfile.csv --output output.csv
        '''
    )

    parser.add_argument(
        '--input',
        default='generated_vignettes_sentence_structure_4cat.json_edit1.csv',
        help='Input CSV file path (default: generated_vignettes_sentence_structure_4cat.json_edit1.csv)'
    )

    parser.add_argument(
        '--output',
        help='Output CSV file path (if not specified, only preview mode will run)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Show preview of vignettes with introductions'
    )

    parser.add_argument(
        '--num-preview',
        type=int,
        default=5,
        help='Number of vignettes to preview (default: 5)'
    )

    args = parser.parse_args()

    # If no output file specified, enable preview mode
    preview_mode = args.preview or (args.output is None)

    add_introductions_to_vignettes(
        input_file=args.input,
        output_file=args.output,
        preview_only=preview_mode,
        num_preview=args.num_preview
    )


if __name__ == "__main__":
    main()
