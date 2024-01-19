import fitz  # PyMuPDF
import os
import json
from Parameters import global_expected_values_folder, global_raw_pdf_folder, global_input_folder


def extract_pdf_page(filename, page_number):

    input_pdf_path = os.path.join(global_input_folder, filename)

    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)

    # Check if the specified page number is within the valid range
    if 0 <= page_number < len(pdf_document):
        # Create a new PDF document
        output_pdf_document = fitz.open()

        # Add the selected page to the new document
        output_pdf_document.insert_pdf(pdf_document, from_page=page_number - 1, to_page=page_number - 1)

        # Construct the output filename for the extracted page
        output_filename = filename

        # Save the extracted page to a new PDF file
        output_pdf_path = os.path.join(global_raw_pdf_folder, output_filename)
        output_pdf_document.save(output_pdf_path)

        # Close the PDF documents
        pdf_document.close()
        output_pdf_document.close()
    else:
        print(f"Invalid page number {page_number} for file {filename}")


def main():
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
        # extract the pdf page
        extract_pdf_page(filename, page)


# Entry point of the program
if __name__ == "__main__":
    main()
