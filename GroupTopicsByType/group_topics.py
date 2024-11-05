import os
import shutil
import re

def organize_files_by_type_and_topic(source_dir):
    # Define a dictionary to map file extensions to folder names
    file_type_dirs = {
        '.pdf': 'PDF',
        '.mp4': 'MP4',
    }

    # Regular expression to identify topic numbers in file names (e.g., "topic 1", "topic 2")
    topic_pattern = re.compile(r'topic[_\s]*(\d+)', re.IGNORECASE)

    # Loop through files in the source directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # Process only files, not directories
        if os.path.isfile(file_path):
            # Extract file extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # Check if the file type has a defined folder (PDF or MP4)
            if ext in file_type_dirs:
                # Search for topic number in the filename
                match = topic_pattern.search(filename)
                
                if match:
                    topic_num = match.group(1)
                    
                    # Define the destination folder structure: {FileType}/{Topic}
                    dest_dir = os.path.join(source_dir, file_type_dirs[ext], f"topic_{topic_num}")
                    
                    # Create the destination directories if they don't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Move the file to the destination directory
                    shutil.move(file_path, os.path.join(dest_dir, filename))
                    print(f"Moved '{filename}' to '{dest_dir}'")
                else:
                    print(f"No topic found in '{filename}', skipping.")
            else:
                print(f"File type for '{filename}' is not supported, skipping.")

# Usage: set your source directory path
source_directory = "E:\\Masters\\Masters\\SCE5201\\Notes\\tmp"
organize_files_by_type_and_topic(source_directory)
