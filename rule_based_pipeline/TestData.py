# ============================================================================================================================
# PDF_Analyzer
# File   : TestData.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================

from DataImportExport import DataImportExport
from Format_Analyzer import Format_Analyzer
from glob import glob
from globals import print_verbose, save_txt_to_file
from TestDataSample import TestDataSample


class TestData:
    """
    TestData class manages a collection of TestDataSample objects for testing purposes.
    It provides methods for filtering, loading data from CSV files, generating dummy test data, and saving to CSV.

    Attributes:
        samples: A list to store instances of TestDataSample.
    """
    samples = None

    # Constants variables
    SRC_FILE_FORMAT_AUTO = 0
    SRC_FILE_FORMAT_OLD = 1
    SRC_FILE_FORMAT_NEW = 2

    def __init__(self):
        self.samples = []

    def filter_kpis(self, by_kpi_id=None, by_data_type=None, by_source_file=None, by_has_fixed_source_file=False):
        samples_new = []
        for s in self.samples:
            keep = True
            if by_kpi_id is not None and s.data_kpi_id not in by_kpi_id:
                keep = False
            if by_data_type is not None and s.data_data_type not in by_data_type:
                keep = False
            if by_has_fixed_source_file and s.fixed_source_file is None:
                keep = False
            if by_source_file is not None and s.data_source_file not in by_source_file:
                keep = False

            if keep:
                samples_new.append(s)

        self.samples = samples_new

    def get_pdf_list(self):
        res = []
        for s in self.samples:
            res.append(s.data_source_file)
        res = list(set(res))
        res = sorted(res, key=lambda s: s.lower())
        return res

    def fix_file_names(self, fix_list):
        for i in range(len(self.samples)):
            for f in fix_list:
                if self.samples[i].data_source_file == f[0]:
                    self.samples[i].fixed_source_file = f[1]
                    break

    def load_from_csv(self, src_file_path, src_file_format=SRC_FILE_FORMAT_AUTO):
        raw_data = ''

        def read_next_cell(p):
            p0 = -1
            p1 = -1
            p2 = -1
            # print("====>> p = "+str(p))
            if raw_data[p:(p + 4)] == '"[""':
                p0 = p + 4
                p1 = raw_data.find('""]"', p + 1)
                p2 = p1 + 4
            elif raw_data[p] == '"':
                p0 = p + 1
                p_cur = p0
                while True:
                    p1 = raw_data.find('"', p_cur)
                    if raw_data[p1 + 1] != '"':
                        break
                    p_cur = p1 + 2

                p2 = p1 + 1
            else:
                p0 = p
                p2_a = raw_data.find(',' if src_file_format == TestData.SRC_FILE_FORMAT_OLD else ';', p)
                p2_b = raw_data.find('\n', p)
                if p2_a == -1:
                    p2 = p2_b
                elif p2_b == -1:
                    p2 = p2_a
                else:
                    p2 = min(p2_a, p2_b)

                p1 = p2
            # print("===>> p1="+str(p1))

            if (p1 == -1 or raw_data[p2] not in (
                    ',' if src_file_format == TestData.SRC_FILE_FORMAT_OLD else ';', '\n')):
                raise ValueError(
                    'No cell delimiter detected after position ' + str(p) + ' at "' + raw_data[p:p + 20] + '..."')

            cell_data = raw_data[p0:p1].replace('\n', ' ')
            # print("===>>>" + cell_data)

            return cell_data, p2 + 1, raw_data[p2] == '\n'

        def read_next_row(p, n):
            res = []
            for i in range(n):
                cell_data, p, is_at_end = read_next_cell(p)
                if i == n - 1:
                    if not is_at_end:
                        raise ValueError(
                            'Row has not ended after position ' + str(p) + ' at "' + raw_data[p:p + 20] + '..."')
                else:
                    if is_at_end:
                        raise ValueError(
                            'Row has ended too early after position ' + str(p) + ' at "' + raw_data[p:p + 20] + '..."')
                res.append(cell_data)

            # print('==>> next row starts at pos '+str(p)  + ' at "'+raw_data[p:p+20]+'..."')
            return res, p

        if src_file_format == TestData.SRC_FILE_FORMAT_AUTO:
            try:
                # try old format:
                print_verbose(2, 'Trying old csv format')
                return self.load_from_csv(src_file_path, TestData.SRC_FILE_FORMAT_OLD)
            except ValueError:
                # try new format:
                print_verbose(2, 'Trying new csv format')
                return self.load_from_csv(src_file_path, TestData.SRC_FILE_FORMAT_NEW)

        self.samples = []

        with open(src_file_path, errors='ignore', encoding="ascii") as f:
            data_lines = f.readlines()

        # print(len(data_lines))
        for i in range(len(data_lines)):
            data_lines[i] = data_lines[i].replace('\n', '')
        raw_data = '\n'.join(data_lines[1:]) + '\n'

        # current format in sample csv file (old-format):
        # Number,Sector,Unit,answer,"comments, questions",company,data_type,irrelevant_paragraphs,kpi_id,relevant_paragraphs,sector,source_file,source_page,year

        # and for new format:
        # Number;company;source_file;source_page;kpi_id;year;answer;data_type;relevant_paragraphs;annotator;sector;comments

        p = 0

        while p < len(raw_data):
            if src_file_format == TestData.SRC_FILE_FORMAT_OLD:
                # parse next row
                row_data, p = read_next_row(p, 14)
                # print(row_data)

                year = Format_Analyzer.to_int_number(row_data[13], 4)
                if not Format_Analyzer.looks_year(str(year)):
                    raise ValueError('Found invalid year "' + str(year) + '" at row ' + str(row_data))

                sample = TestDataSample()
                sample.data_number = Format_Analyzer.to_int_number(row_data[0])  # 0
                sample.data_sector = row_data[1]  # ''
                sample.data_unit = row_data[2]  # ''
                sample.data_answer = row_data[3]  # ''
                sample.data_comments_questions = row_data[4]  # ''
                sample.data_company = row_data[5]  # ''
                sample.data_data_type = row_data[6]  # ''
                sample.data_irrelevant_paragraphs = row_data[7]  # ''
                sample.data_kpi_id = Format_Analyzer.to_int_number(row_data[8])  # 0
                sample.data_relevant_paragraphs = row_data[9]  # ''
                sample.data_sector = row_data[10]  # ''
                sample.data_source_file = row_data[11]  # ''
                sample.data_source_page = Format_Analyzer.to_int_number(row_data[12])  # 0
                sample.data_year = year  # 0

                self.samples.append(sample)

            if src_file_format == TestData.SRC_FILE_FORMAT_NEW:
                # parse next row
                row_data, p = read_next_row(p, 12)
                # print(row_data)

                year = Format_Analyzer.to_int_number(row_data[5], 4)
                if not Format_Analyzer.looks_year(str(year)):
                    raise ValueError('Found invalid year "' + str(year) + '" at row ' + str(row_data))

                sample = TestDataSample()
                sample.data_number = Format_Analyzer.to_int_number(row_data[0])  # 0
                sample.data_sector = row_data[10]  # ''
                sample.data_unit = 'N/A'
                sample.data_answer = row_data[6]  # ''
                sample.data_comments_questions = row_data[11]  # ''
                sample.data_company = row_data[1]  # ''
                sample.data_data_type = row_data[7]  # ''
                sample.data_irrelevant_paragraphs = 'N/A'
                sample.data_kpi_id = Format_Analyzer.to_float_number(row_data[4])  # 0
                sample.data_relevant_paragraphs = row_data[8]  # ''
                sample.data_source_file = row_data[2]  # ''
                sample.data_source_page = Format_Analyzer.to_int_number(row_data[3])  # 0
                sample.data_year = year  # 0

                self.samples.append(sample)

    def save_to_csv(self, dst_file_path):
        save_txt_to_file(TestDataSample.samples_to_csv(self.samples), dst_file_path)

    def get_unique_list_of_pdf_files(self):
        """
        Get a list of unique fixed_source_file values from TestDataSample objects.

        Returns:
            list: A sorted list of unique fixed_source_file values.
        """
        fixed_files = [sample.fixed_source_file for sample in self.samples]
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
        sample.data_number = count
        sample.data_sector = 'N/A'
        sample.data_unit = 'N/A'
        sample.data_answer = 'N/A'
        sample.data_comments_questions = 'N/A'
        sample.data_company = 'N/A'
        sample.data_data_type = 'N/A'
        sample.data_irrelevant_paragraphs = 'N/A'
        sample.data_kpi_id = 0
        sample.data_relevant_paragraphs = 'N/A'
        sample.data_sector = 'N/A'
        sample.data_source_file = file_name
        sample.fixed_source_file = file_name
        sample.data_source_page = 0
        sample.data_year = 1900
        return sample

    def __repr__(self):
        """
        Returns a string representation of the TestData object.

        Returns:
            str: A string representation of the TestData object.
        """
        return TestDataSample.samples_to_string(self.samples)
