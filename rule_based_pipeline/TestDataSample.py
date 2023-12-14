# ============================================================================================================================
# PDF_Analyzer
# File   : TestDataSample.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable
from Format_Analyzer import Format_Analyzer


# TODO:I think we don't need this class! -> delete or need refactor
class TestDataSample:
    """
    Class representing a data sample for testing.

    Attributes:
        data_number (int): The data number.
        data_sector (str): The data sector.
        data_unit (str): The data unit.
        data_answer (str): The data answer.
        data_comments_questions (str): Comments and questions associated with the data.
        data_company (str): The data company.
        data_data_type (str): The data type.
        data_irrelevant_paragraphs (str): Irrelevant paragraphs related to the data.
        data_kpi_id (int): The KPI ID.
        data_relevant_paragraphs (str): Relevant paragraphs related to the data.
        data_source_file (str): The source file of the data.
        data_source_page (int): The source page of the data.
        data_year (int): The year associated with the data.
        fixed_source_file: Additional source file information.

    Methods:
        __init__: Initializes an instance of the TestDataSample class.
        __repr__: Returns a string representation of the TestDataSample instance.
        samples_to_string: Converts a list of TestDataSample instances to a formatted string.
        samples_to_csv: Converts a list of TestDataSample instances to a CSV-formatted string.
    """

    def __init__(self):
        """
        Initializes an instance of the TestDataSample class with default values.
        """
        self.data_number = 0
        self.data_sector = ''
        self.data_unit = ''
        self.data_answer = ''
        self.data_comments_questions = ''
        self.data_company = ''
        self.data_data_type = ''
        self.data_irrelevant_paragraphs = ''
        self.data_kpi_id = 0
        self.data_relevant_paragraphs = ''
        self.data_sector = ''
        self.data_source_file = ''
        self.data_source_page = 0
        self.data_year = 0
        self.fixed_source_file = None

    @staticmethod
    def samples_to_string(lst, max_width=140, min_col_width=5):
        """
        Converts a list of TestDataSample instances to a formatted string.

        Args:
            lst (list): List of TestDataSample instances.
            max_width (int): Maximum width of the output string.
            min_col_width (int): Minimum width of each column.

        Returns:
            str: Formatted string representation of the TestDataSample instances.
        """
        console_table = ConsoleTable(14)
        console_table.cells.extend(
            ['NUMBER', 'SECTOR', 'UNIT', 'ANSWER', 'COMMENTS', 'COMPANY', 'DATA_TYPE', 'IRREL_PARAG', 'KPI_ID',
             'RELEV_PARAG', 'SECTOR', 'SOURCE_FILE', 'SOURCE_PAGE', 'YEAR'])

        for k in lst:
            console_table.cells.extend([
                str(k.data_number), str(k.data_sector), str(k.data_unit), str(k.data_answer),
                str(k.data_comments_questions), str(k.data_company), str(k.data_data_type),
                str(k.data_irrelevant_paragraphs), str(k.data_kpi_id), str(k.data_relevant_paragraphs),
                str(k.data_sector), str(k.data_source_file), str(k.data_source_page), str(k.data_year)
            ])

        return console_table.to_string(max_width, min_col_width)

    @staticmethod
    def samples_to_csv(lst):
        """
        Converts a list of TestDataSample instances to a CSV-formatted string.

        Args:
            lst (list): List of TestDataSample instances.

        Returns:
            str: CSV-formatted string representation of the TestDataSample instances.
        """

        def escape(txt):
            txt = txt.replace("\n", "")
            txt = txt.replace("\r", "")
            txt = txt.replace('"', '""')
            return '"' + Format_Analyzer.trim_whitespaces(txt) + '"'

        result = ""
        for k in lst:
            result += escape(str(k.data_number)) + ";"
            result += escape(str(k.data_sector)) + ";"
            result += escape(str(k.data_unit)) + ";"
            result += escape(str(k.data_answer)) + ";"
            result += escape(str(k.data_comments_questions)) + ";"
            result += escape(str(k.data_company)) + ";"
            result += escape(str(k.data_data_type)) + ";"
            result += escape(str(k.data_irrelevant_paragraphs)) + ";"
            result += escape(str(k.data_kpi_id)) + ";"
            result += escape(str(k.data_relevant_paragraphs)) + ";"
            result += escape(str(k.data_sector)) + ";"
            result += escape(str(k.data_source_file)) + ";"
            result += escape(str(k.data_source_page)) + ";"
            result += escape(str(k.data_year)) + "\n"

        return result

    def __repr__(self):
        """
        Returns a string representation of the TestDataSample instance.

        Returns:
            str: String representation of the TestDataSample instance.
        """
        return TestDataSample.samples_to_string([self])
