import os
import zipfile
import shutil

from pathlib import Path

ZIPPED_DIR = Path("ZippedData")
DATA_DIR = Path("Data")

# If Data/ already exists, do nothing
if DATA_DIR.exists():
    print("Data folder already exists. Skipping extraction.")
    exit(0)

# Create the Data/ folder
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Loop through each .zip file in ZippedData/
for zip_path in ZIPPED_DIR.glob("*.zip"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract to a temporary folder
        temp_extract_path = ZIPPED_DIR / "temp_extracted"
        zip_ref.extractall(temp_extract_path)

        # Find all data files in the extracted folder
        for root, dirs, files in os.walk(temp_extract_path):
            for file in files:
                if file.endswith((".csv", ".json", ".xlsx", ".xls", ".sqlite", ".db", ".txt")):
                    full_file_path = Path(root) / file
                    dest_file_path = DATA_DIR / file

                    # Avoid overwriting files with same names
                    if dest_file_path.exists():
                        print(f"File {file} already exists in Data/. Skipping.")
                    else:
                        shutil.copy2(full_file_path, dest_file_path)
                        print(f"Extracted: {file}")

        # Clean up extracted temp folder after each .zip
        shutil.rmtree(temp_extract_path)

print("All zipped data extracted into Data/ folder.")
