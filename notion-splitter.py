import os
from pathlib import Path
import shutil

def get_unique_filename(directory, base_name, extension):
    """Generate a unique filename by adding a number suffix if needed."""
    counter = 1
    new_path = directory / f"{base_name}{extension}"
    
    while new_path.exists():
        new_path = directory / f"{base_name}_{counter}{extension}"
        counter += 1
    
    return new_path.name

def normalize_name(name):
    """Convert spaces to underscores for comparison purposes."""
    return name.replace(' ', '_')

def process_files():
    # Create input and output directories if they don't exist
    input_dir = Path('input')
    output_dir = Path('output')
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # First pass: Rename markdown files and collect base names
    all_base_names = set()
    md_files = {}  # Store markdown files and their new names
    used_names = set()  # Keep track of names we've already assigned
    
    # First collect all existing base names (without hashes)
    for file_path in input_dir.iterdir():
        base_name = file_path.stem  # Get filename without extension
        extension = file_path.suffix.lower()
        
        # If it's a markdown file with a hash, get the name without hash
        if extension == '.md' and len(base_name) > 33 and ' ' in base_name:
            base_name = base_name[:-33]
        
        # Add normalized base name to set (without extension)
        all_base_names.add(normalize_name(base_name))
    
    # Second, process the files that need renaming
    for file_path in input_dir.iterdir():
        base_name = file_path.stem
        extension = file_path.suffix.lower()
        
        # If it's a markdown file with a hash (more than 33 chars)
        if extension == '.md' and len(base_name) > 33 and ' ' in base_name:
            # Remove the hash (last 33 characters including space)
            new_base = base_name[:-33]
            
            # Generate unique name considering both existing files and names we've already assigned
            counter = 1
            new_name = f"{new_base}.md"
            while (input_dir / new_name).exists() or new_name in used_names:
                new_name = f"{new_base}_{counter}.md"
                counter += 1
            
            used_names.add(new_name)
            print(f"Renaming {base_name} to {new_name}...")
            md_files[file_path] = new_name
    
    # Third pass: Rename markdown files and check for duplicates
    for old_path, new_name in md_files.items():
        # Get the base name (without extension) from the new name
        new_base_name = Path(new_name).stem
        normalized_base = normalize_name(new_base_name)
        
        # Check if there are other files with the same base name but different extensions
        has_duplicate = False
        for file_path in input_dir.iterdir():
            if (normalize_name(file_path.stem) == normalized_base and 
                file_path.suffix.lower() != '.md' and 
                file_path != old_path):
                has_duplicate = True
                break
        
        if has_duplicate:
            # Move to output directory and ensure unique filename
            new_name = get_unique_filename(output_dir, new_base_name, '.md')
            new_path = output_dir / new_name
            print(f"Moving {new_name} to output directory...")
        else:
            # Keep in input directory
            new_path = input_dir / new_name
            
        print(f"Renaming {old_path.name} to {new_path.name}")
        old_path.rename(new_path)

if __name__ == '__main__':
    process_files()
    print("Done!")
