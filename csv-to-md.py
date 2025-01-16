import csv
import os
from pathlib import Path

def sanitize_filename(filename):
    # Replace invalid filename characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def process_csv_file(csv_path, output_dir):
    # Keep track of how many times we've seen each name
    name_counters = {}
    untitled_counter = 1
    total_rows = 0
    written_files = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            total_rows += 1
            # CHANGE THESE TO MATCH YOUR CSV
            name = row['Name'].strip()
            category = row['MAIN CATEGORY'].strip()
            type_val = row['MAIN TYPE'].strip()
            url = row['URL'].strip()
            
            # Generate filename
            if not name or name.upper() == "UNTITLED":
                filename = f"Untitled_{untitled_counter}"
                untitled_counter += 1
            else:
                # If we've seen this name before, add a counter
                if name in name_counters:
                    name_counters[name] += 1
                    filename = f"{name}_{name_counters[name]}"
                else:
                    name_counters[name] = 0
                    filename = name
            
            # Sanitize filename and add .md extension
            filename = sanitize_filename(filename) + '.md'
            
            # Create markdown content
            content = []
            content.append(f"Category: {category}")
            if type_val:  # Only include type if not empty
                content.append(f"Type: {type_val}")
            content.append(f"URL: {url}")
            
            # Write to markdown file
            output_path = output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write('\n'.join(content))
            written_files += 1
    
    print(f"Processed {total_rows} rows")
    print(f"Wrote {written_files} files")
    if total_rows != written_files:
        print(f"Warning: {total_rows - written_files} rows were not written to unique files")

def process_input_directory():
    # Create input and output directories if they don't exist
    input_dir = Path('input')
    output_dir = Path('output')
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Get all CSV files from input directory
    csv_files = list(input_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in the input directory!")
        return
    
    # Process each CSV file
    for csv_path in csv_files:
        print(f"Processing {csv_path.name}...")
        process_csv_file(csv_path, output_dir)
        print(f"Finished processing {csv_path.name}")

if __name__ == '__main__':
    process_input_directory()
