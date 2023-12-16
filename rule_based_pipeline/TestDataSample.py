# ============================================================================================================================
# PDF_Analyzer
# File   : TestDataSample.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable
from Format_Analyzer import Format_Analyzer


class TestDataSample:
    """
    Class representing a data sample for testing.

    Attributes:
        kpi_id (int): The kpi id.
        kpi_name (str): The name of kpi.
        src_file (str): The source file.
        page_num (int): The number of page.
        item_ids (list): The ids of items.
        pos_x (float): The x position for items.
        pos_y (float): The y position for items.
        raw_txt (str): The row of text.
        year (int): The year ...
        value (int): ...
        score (int): ...
        unit (str): ...
        match_type (str): ...

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
        self.kpi_id = 0
        self.kpi_name = ''
        self.src_file = ''
        self.page_num = 0
        self.item_ids = []
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.raw_txt = ''
        self.year = 0
        self.value = 0
        self.score = 0
        self.unit = ''
        self.match_type = 0

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
        console_table = ConsoleTable(13)
        console_table.cells.extend(
            ['KPI_ID', 'KPI_NAME', 'SRC_FILE', 'PAGE_NUM', 'ITEM_IDS', 'POS_X', 'POS_Y', 'RAW_TXT', 'YEAR', 'VALUE',
             'SCORE', 'UNIT', 'MATCH_TYPE'])

        for k in lst:
            console_table.cells.extend([
                str(k.kpi_id), str(k.kpi_name), str(k.src_file), str(k.page_num), str(k.item_ids), str(k.pos_x),
                str(k.pos_y), str(k.raw_txt), str(k.year), str(k.value), str(k.score), str(k.unit), str(k.match_type)
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
            result += escape(str(k.kpi_id)) + ";"
            result += escape(str(k.kpi_name)) + ";"
            result += escape(str(k.src_file)) + ";"
            result += escape(str(k.page_num)) + ";"
            result += escape(str(k.item_ids)) + ";"
            result += escape(str(k.pos_x)) + ";"
            result += escape(str(k.pos_y)) + ";"
            result += escape(str(k.raw_txt)) + ";"
            result += escape(str(k.year)) + ";"
            result += escape(str(k.value)) + ";"
            result += escape(str(k.score)) + ";"
            result += escape(str(k.unit)) + ";"
            result += escape(str(k.match_type)) + "\n"

        return result

    def __repr__(self):
        """
        Returns a string representation of the TestDataSample instance.

        Returns:
            str: String representation of the TestDataSample instance.
        """
        return TestDataSample.samples_to_string([self])
