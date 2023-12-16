# ============================================================================================================================
# PDF_Analyzer
# File   : TestData.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================
from DataImportExport import DataImportExport
import csv
from Format_Analyzer import Format_Analyzer
from glob import glob
from globals import print_verbose, save_txt_to_file
from io import StringIO
from TestDataSample import TestDataSample


class TestData:
    """
    TestData class manages a collection of TestDataSample objects for testing purposes.
    It provides methods for filtering, loading data from CSV files, generating dummy test data, and saving to CSV.

    Attributes:
        samples: A list to store instances of TestDataSample.
    """
    samples = None

    def __init__(self):
        """
        Initializes an instance of the TestData class.
        """
        self.samples = []

    def filter_kpis(self, by_kpi_id=None, by_source_file=None, by_has_fixed_source_file=False):
        """
        Filters TestData samples based on specified criteria.

        Args:
            by_kpi_id (list): List of KPI IDs to filter by.
            by_source_file (list): List of source files to filter by.
            by_has_fixed_source_file (bool): Flag to filter samples with fixed source files.

        Returns:
            None
        """
        samples_new = []
        for s in self.samples:
            keep = True

            if by_kpi_id is not None and s.kpi_id not in by_kpi_id:
                keep = False

            if by_source_file is not None and s.src_file not in by_source_file:
                keep = False

            if by_has_fixed_source_file and s.src_file is None:
                keep = False

            if keep:
                samples_new.append(s)

        self.samples = samples_new

    def get_pdf_list(self):
        """
        Get a list of PDF files from TestData samples.

        Returns:
            list: A list of PDF file names.
        """
        result = [s.data_source_file for s in self.samples]
        result = list(set(result))
        result = sorted(result, key=lambda s: s.lower())
        return result

    def fix_file_names(self, fix_list):
        """
        Fixes TestData sample file names based on the provided fix list.

        Args:
            fix_list (list): List of tuples containing old and new file names.

        Returns:
            None
        """
        for i in range(len(self.samples)):
            for f in fix_list:
                if self.samples[i].data_source_file == f[0]:
                    self.samples[i].fixed_source_file = f[1]
                    break

    def load_from_csv(self, src_file_path):
        """
        Loads TestData samples from a CSV file.

        Args:
            src_file_path (str): Path to the CSV file.

        Returns:
            None
        """

        self.samples = []

        with open(src_file_path, errors='ignore', encoding="ascii") as f:
            data_lines = f.readlines()

        for i in range(len(data_lines)):
            data_lines[i] = data_lines[i].replace('\n', '')

        raw_data = data_lines[1:]

        result_list_of_lists = []

        for input_string in raw_data:
            csv_reader = csv.reader(StringIO(input_string))
            result_list = next(csv_reader)
            result_list_of_lists.append(result_list)

        for result_list in result_list_of_lists:
            year = Format_Analyzer.to_int_number(result_list[8], 4)
            if not Format_Analyzer.looks_year(str(year)):
                raise ValueError('Found invalid year "' + str(year) + '" at row ' + str(result_list))

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
            sample.value = Format_Analyzer.to_float_number(result_list[9])
            sample.score = result_list[10]
            sample.unit = result_list[11]
            sample.match_type = result_list[12]

            self.samples.append(sample)

    def save_to_csv(self, dst_file_path):
        """
        Saves TestData samples to a CSV file.

        Args:
            dst_file_path (str): Path to the destination CSV file.

        Returns:
            None
        """
        save_txt_to_file(TestDataSample.samples_to_csv(self.samples), dst_file_path)

    def get_unique_list_of_pdf_files(self):
        """
        Get a list of unique fixed_source_file values from TestDataSample objects.

        Returns:
            list: A sorted list of unique fixed_source_file values.
        """
        fixed_files = [sample.src_file for sample in self.samples]

        unique_fixed_files = list(set(fixed_files))

        sorted_unique_fixed_files = sorted(unique_fixed_files, key=lambda sample: sample.lower())

        return sorted_unique_fixed_files

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
            result.extend(Format_Analyzer.extract_file_path(file_path))
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
            if file_name != Format_Analyzer.cleanup_filename(file_name):
                print_verbose(1, "Warning: Bad filename: '" + file_name + "' - this file will be skipped")
                continue

            # Create a TestDataSample object with dummy data
            sample = self.dummy_data_sample_factory(count, file_name)

            # Add the TestDataSample to the TestData object
            self.samples.append(sample)
            count += 1

        # Save paths of the pdf files to a JSON file named 'info.json' using DataImportExport
        DataImportExport.save_path_files_to_json_file(file_paths)

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
