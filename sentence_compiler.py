import json
import pandas as pd

def load_json_file(filename):
    """Helper function to load a JSON file with error handling."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure it is in the same directory as the script.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
        return None

def build_vignettes_spreadsheet():
    """
    Loads sentence bank and vignette structures, builds all vignettes,
    and saves them to CSV and Excel files.
    """
    
    # IMPORTANT: Change the file name here based on the type of structure required
    # E.G. 'sentence_structure1.json' or 'sentence_structure2.json'
    structure_doc = 'sentence_structure_4cat.json'
    # 1. Load the data files
    sentence_bank = load_json_file('sentences.json')
    # IMPORTANT: Change the file name here based on the type of structure required
    # E.G. 'sentence_structure1.json' or 'sentence_structure2.json'
    vignette_structures = load_json_file(f'{structure_doc}')
    # Load avatar names
    avatar_names = load_json_file('avatar_names.json')

    structure_basename = structure_doc.replace('.json', '')

    # Exit if files failed to load
    if not sentence_bank or not vignette_structures or not avatar_names:
        return

    print("Successfully loaded sentences, structure, and avatar names.")
    
    # This list will hold all the row data for our spreadsheet
    all_vignette_data = []
    
    # 2. Iterate through each Group (e.g., "Group 1", "Group 2", ...)
    for group_name, vignette_list in vignette_structures.items():
        
        print(f"Processing {group_name}...")

        # 3. Create a new set of counters for this Group (as requested)
        category_counters = {category: 0 for category in sentence_bank.keys()}

        # 4. Iterate through each vignette recipe in the current group
        for recipe in vignette_list:
            avatar = recipe['avatar']
            categories = recipe['categories']

              # Get the name for this avatar
            avatar_name = avatar_names.get(avatar, "UNKNOWN NAME")
            
             # This list will hold all data for a single row
            current_row_data = [group_name, avatar, avatar_name]
            
            # This list will just hold the sentences for the final column
            full_vignette_sentences = []

            # 5. Build the row cell by cell for each sentence
            for category in categories:
                if category not in sentence_bank:
                    print(f"Warning: Category '{category}' not found. Skipping.")
                    current_row_data.extend(["CATEGORY NOT FOUND", -1, ""])
                    continue
                
                sentence_list = sentence_bank[category]
                current_index = category_counters[category]
                sentence_to_use_index = current_index % len(sentence_list)
                sentence = sentence_list[sentence_to_use_index]
                
                # Add the 3 "construction" columns for this sentence
                current_row_data.append(category)             # e.g., "Immobility"
                current_row_data.append(sentence_to_use_index) # e.g., 0
                current_row_data.append(sentence)              # e.g., "I feel my muscles..."
                
                # Add to our temporary list for the final paragraph
                full_vignette_sentences.append(sentence)
                
                # 6. Increment the counter for this category
                category_counters[category] += 1
            
            # 7. Add the final constructed vignette to the end of the row
            final_paragraph = " ".join(full_vignette_sentences)
            current_row_data.append(final_paragraph)
            
            # Add this completed row to our main data list
            all_vignette_data.append(current_row_data)

    # 8. Create the final DataFrame
    
    # Define the column headers
    column_names = [
        "Group", "Avatar", "Name",
        "Category 1", "Index 1", "Sentence 1",
        "Category 2", "Index 2", "Sentence 2",
        "Category 3", "Index 3", "Sentence 3",
        "Category 4", "Index 4", "Sentence 4",
        "Full Vignette"
    ]
    # Create the pandas DataFrame
    df = pd.DataFrame(all_vignette_data, columns=column_names)

    # 9. Save the DataFrame to files
    csv_filename = f"generated_vignettes_{structure_doc}_edit1.csv"
    excel_filename = f"generated_vignettes_{structure_doc}_edit1.xlsx"

    try:
        # Save to CSV
        # encoding='utf-8-sig' helps Excel open CSVs with special characters
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"\nSuccessfully saved CSV file: '{csv_filename}'")
        
        # Save to Excel
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"Successfully saved Excel file: '{excel_filename}'")

    except Exception as e:
        print(f"\nAn error occurred while saving the files: {e}")

# --- Run the script ---
if __name__ == "__main__":
    build_vignettes_spreadsheet()