import os
import json
from config_for_rb import global_expected_values_folder

# Initialize a dictionary to store unique pages along with their corresponding JSON file names
unique_pages = {}

# Loop through each file in the directory
for filename in os.listdir(global_expected_values_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(global_expected_values_folder, filename)

        # change the extension .json to .pdf
        filename = filename.replace(".json", ".pdf")

        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Loop through each "Page" value in the JSON data
            for page in set(data["Scope 1"]["Page"] + data["Scope 2"]["Page"] + data["Scope 3"]["Page"]):
                # Check if the page is not already in the dictionary
                if page not in unique_pages:
                    # Add the page to the dictionary with the corresponding filename
                    unique_pages[page] = filename

# Print the result
for page, filename in unique_pages.items():
    print(f'File: {filename}, Page: {page}')
