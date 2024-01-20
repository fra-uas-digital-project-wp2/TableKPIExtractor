# ============================================================================================================================
# PDF_Analyzer
# File   : TestData.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================
import csv
import jsonpickle

from FormatAnalyzer import FormatAnalyzer
from glob import glob
import config_for_rb 
from globals import print_verbose, save_txt_to_file, remove_trailing_slash
from io import StringIO
from TestDataSample import TestDataSample


class TestData:
    """
    TestData class manages a collection of TestDataSample objects for testing purposes.
    It provides methods for filtering, loading data from CSV files, generating dummy test data, and saving to CSV.

    Attributes:
        samples: A list to store instances of TestDataSample.
    """

    def __init__(self):
        """
        Initializes an instance of the TestData class.
        """
        self.samples = []

    def filter_kpis(self, by_kpi_id=None, by_source_file=None):
        """
        Filters TestData samples based on specified criteria.

        Args:
            by_kpi_id (list, optional): List of KPI IDs to filter by.
            by_source_file (list, optional): List of source files to filter by.

        Returns:
            None
        """
        # Create a new list to store filtered samples
        filtered_samples = []

        # Iterate through each TestData sample
        for sample in self.samples:
            keep = True  # Flag to determine whether to keep the sample or not

            # Check if filtering by KPI ID and the sample's KPI ID is not in the specified list
            if by_kpi_id is not None and sample.kpi_id not in by_kpi_id:
                keep = False

            # Check if filtering by source file and the sample's source file is not in the specified list
            if by_source_file is not None and sample.src_file not in by_source_file:
                keep = False

            # If all criteria are met, keep the sample by appending it to the filtered list
            if keep:
                filtered_samples.append(sample)

        # Update the TestData samples with the filtered list
        self.samples = filtered_samples

    def get_unique_list_of_pdf_files(self):
        """
        Get a list of unique PDF files values from TestDataSample objects.

        Returns:
            list: A sorted list of unique PDF files values.
        """
        # Extract PDF file names from TestData samples
        pdf_files = [sample.src_file for sample in self.samples]

        # Remove duplicate entries by converting the list to a set and back to a list
        unique_pdf_files = list(set(pdf_files))

        # Sort the list of unique PDF file names in a case-insensitive manner
        sorted_pdf_files = sorted(unique_pdf_files, key=lambda sample: sample.lower())

        return sorted_pdf_files

    def load_from_csv(self, src_file_path):
        """
        Loads TestData samples from a CSV file.

        Args:
            src_file_path (str): Path to the CSV file.

        Returns:
            None
        """

        # Initialize TestData samples list
        #self.samples = [] # TODO Add this line into the 

        # Read all lines from the CSV file
        with open(src_file_path, errors='ignore', encoding="ascii") as file:
            data_lines = file.readlines()

        # Remove newline characters from each line
        data_lines = [line.replace('\n', '') for line in data_lines]

        # Extract raw data excluding the header
        raw_data = data_lines[1:]

        # Process each line of raw data
        result_list_of_lists = []
        for input_string in raw_data:
            # Use csv.reader to handle CSV format
            csv_reader = csv.reader(StringIO(input_string))
            result_list = next(csv_reader)
            result_list_of_lists.append(result_list)

        # Create TestDataSample objects from processed data
        for result_list in result_list_of_lists:
            # Convert year to integer, validating its format
            year = FormatAnalyzer.to_int_number(result_list[8], 4)
            if not FormatAnalyzer.looks_year(str(year)):
                raise ValueError('Found invalid year "' + str(year) + '" at row ' + str(result_list))

            # Create TestDataSample object and populate its attributes
            sample = TestDataSample()
            sample.kpi_id = result_list[0]
            sample.kpi_name = result_list[1]
            sample.src_file = result_list[2]
            sample.page_num = result_list[3]
            sample.item_ids = result_list[4]
            sample.pos_x = result_list[5]
            sample.pos_y = result_list[6]
            sample.raw_txt = result_list[7]
            sample.year = year
            try:
                sample.value = FormatAnalyzer.to_float_number(result_list[9])
            except:
                sample.value = 0
            sample.score = result_list[10]
            sample.unit = result_list[11]
            sample.match_type = result_list[12]

            # Add the TestDataSample to the TestData samples list
            self.samples.append(sample)

    def save_to_csv(self, dst_file_path):
        """
        Saves TestData samples to a CSV file.

        Args:
            dst_file_path (str): Path to the destination CSV file.

        Returns:
            None
        """
        # Convert TestData samples to CSV format and save to file
        save_txt_to_file(TestDataSample.samples_to_csv(self.samples), dst_file_path)

    def generate_dummy_test_data(self, pdf_folder, pdf_filter='*'):
        """
        Generates dummy test data by populating samples with information from PDF files in a specified folder.

        Args:
            pdf_folder (str): Path to the folder containing PDF files.
            pdf_filter (str): Filter for PDF files (default is '*').

        Returns:
            None
        """

        def extract_file_info(file_path):
            """
            Extracts file information (path, name and extension of the file) using Format_Analyzer.

            Args:
                file_path (str): Path to the PDF file.

            Returns:
                list: A list containing the path, name and extension of the file

            Example: raw_pdf/filename.pdf
                ['raw_pdf/', 'filename', 'pdf']
            """
            result = [file_path]
            result.extend(FormatAnalyzer.extract_file_path(file_path))
            return result

        # Use glob to get a list of PDF file paths in the given folder (*/raw_pdf)
        file_paths = glob(pdf_folder + '/**/' + pdf_filter + '.pdf', recursive=True)

        # Convert Windows-style paths to Unix-style paths and extract file information (path, name and extension)
        file_paths = [extract_file_info(f.replace('\\', '/')) for f in file_paths]

        count = 0
        for file_info in file_paths:
            # create the file name based on file_info
            file_name = file_info[2] + '.' + file_info[3]

            # Check if the filename needs cleanup; print a warning and skip the file if necessary
            if file_name != FormatAnalyzer.cleanup_filename(file_name):
                print_verbose(1, "Warning: Bad filename: '" + file_name + "' - this file will be skipped")
                continue

            # Create a TestDataSample object with dummy data
            sample = self.dummy_data_sample_factory(count, file_name)

            # Add the TestDataSample to the TestData object
            self.samples.append(sample)
            count += 1

        # Save paths of the pdf files to a JSON file named 'info.json' using DataImportExport
        self.save_path_files_to_json_file(file_paths)

    @staticmethod
    def save_path_files_to_json_file(file_paths):
        """
        Saves paths of the files to a JSON file named 'info.json'.

        Args:
            file_paths (list): A list of file paths.

        Returns:
            None
        """
        info_file_contents = {}

        for file_info in file_paths:
            # save paths of the files to info_file_contents:
            # example: "raw_pdf/example.pdf": "raw_pdf/example.pdf"
            info_file_contents[file_info[0]] = file_info[0]

        # Set up jsonpickle options for encoding
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)

        # Encode the info_file_contents dictionary into JSON format
        json_data = jsonpickle.encode(info_file_contents)

        # Construct the file path for the 'info.json' file
        info_file_path = remove_trailing_slash(config_for_rb.global_working_folder) + '/info.json'

        # Write the JSON data to the 'info.json' file
        with open(info_file_path, "w") as info_file:
            info_file.write(json_data)

    @staticmethod
    def dummy_data_sample_factory(count, file_name):
        """
        Create a TestDataSample object with dummy data.

        Args:
            count (int): The data_number for the TestDataSample.
            file_name (str): The data_source_file and fixed_source_file for the TestDataSample.

        Returns:
            TestDataSample: The TestDataSample object with dummy data.
        """
        sample = TestDataSample()
        sample.kpi_id = count
        sample.src_file = file_name
        sample.page_num = 0
        sample.item_ids = []
        sample.pos_x = 0.0
        sample.pos_y = 0.0
        sample.raw_txt = ''
        sample.year = 'N/A'
        sample.data_kpi_id = 1900
        sample.value = 0
        sample.score = 0
        sample.unit = 'N/A'

        return sample

    def __repr__(self):
        """
        Returns a string representation of the TestData object.

        Returns:
            str: A string representation of the TestData object.
        """
        return TestDataSample.samples_to_string(self.samples)
