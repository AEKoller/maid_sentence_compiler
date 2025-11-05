# Vignette Introduction Generator

This tool automatically generates personalized introductions for vignettes based on the participant's name, avatar code (which contains demographic information), and group assignment.

## Features

- **Automatic Introduction Generation**: Creates natural-sounding introductions using the person's name, age, and gender
- **Multiple Template Variations**: Uses randomized templates to create diverse introductions
- **Demographic Extraction**: Automatically extracts age and gender information from avatar codes
- **Preview Mode**: Test the tool and see examples before generating the full output
- **Multiple Output Formats**: Saves results in both CSV and Excel formats

## Avatar Code Format

The tool extracts demographic information from avatar codes:
- **Format**: `[Ethnicity][Gender]-[Age]`
- **Example**: `AM-O` = Asian Male - Older age
  - First letter: A=Asian, B=Black, H=Hispanic, W=White
  - Second letter: M=Male, F=Female
  - After dash: M=Middle age (60s), O=Older age (70s-80s)

## Usage

### Preview Mode (Recommended First Step)

Preview the first 5 vignettes with introductions:
```bash
python vignette_introduction_generator.py --preview
```

Preview more examples (e.g., 10 vignettes):
```bash
python vignette_introduction_generator.py --preview --num-preview 10
```

### Generate and Save Output

Generate introductions for all vignettes and save to a new file:
```bash
python vignette_introduction_generator.py --output vignettes_with_introductions.csv
```

Use a different input file:
```bash
python vignette_introduction_generator.py --input myfile.csv --output output.csv
```

### Command-Line Options

- `--input FILE`: Specify input CSV file (default: `generated_vignettes_sentence_structure_4cat.json_edit1.csv`)
- `--output FILE`: Specify output CSV file (also creates .xlsx automatically)
- `--preview`: Show preview without saving
- `--num-preview N`: Number of vignettes to preview (default: 5)

## Example Output

**Original Vignette:**
> The nursing home has never felt like home — in here, nothing carries my memories...

**With Introduction:**
> My name is Paul, and I'm a man in my early 80s. The nursing home has never felt like home — in here, nothing carries my memories...

## Introduction Templates

The tool uses several template variations:
- "My name is [Name], and I'm a [gender] [age]."
- "I'm [Name], a [gender] [age]."
- "My name is [Name]. I'm [age], and I've been dealing with a terminal illness."
- "I'm [Name]. I'm a [gender] [age], and this is my story."

Templates are randomly selected to provide variety across vignettes.

## Output

The tool creates a new column called "Vignette with Introduction" that contains the complete vignette with the introduction prepended. The output files include:
- CSV file (specified with `--output`)
- Excel file (automatically created with the same name but .xlsx extension)

## Requirements

```bash
pip install pandas openpyxl
```

## Notes

- The tool preserves all original columns in the output
- The new "Vignette with Introduction" column is inserted before the "Full Vignette" column
- Age and gender are intelligently extracted from avatar codes
- Random selection ensures natural variation in introductions
