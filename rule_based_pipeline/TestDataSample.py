# ============================================================================================================================
# PDF_Analyzer
# File   : TestDataSample.py
# Author : Ismail Demir (G124272)
# Date   : 02.08.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable


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
        value (int): The value
        score (int): The score
        unit (str): ...
        match_type (str): ...
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
    def samples_to_csv(samples):
        """
        Converts a list of TestDataSample instances to a CSV-formatted string.

        Args:
            samples (list): List of TestDataSample objects.

        Returns:
            str: CSV-formatted string representation of the TestDataSample instances.
        """

        # Create header row for the CSV
        header = [
            "KPI_ID", "KPI_NAME", "SRC_FILE", "PAGE_NUM", "ITEM_IDS", "POS_X",
            "POS_Y", "RAW_TXT", "YEAR", "VALUE", "SCORE", "UNIT", "MATCH_TYPE"
        ]

        # Create CSV rows from TestDataSample attributes
        rows = [
            [
                str(sample.kpi_id), sample.kpi_name, sample.src_file, str(sample.page_num),
                sample.item_ids, str(sample.pos_x), str(sample.pos_y), sample.raw_txt,
                str(sample.year), str(sample.value), sample.score, sample.unit, sample.match_type
            ]
            for sample in samples
        ]

        # Combine header and rows into a CSV-formatted string
        csv_data = [";".join(header)] + [";".join(row) for row in rows]
        return "\n".join(csv_data)

    def __repr__(self):
        """
        Returns a string representation of the TestDataSample instance.

        Returns:
            str: String representation of the TestDataSample instance.
        """
        return TestDataSample.samples_to_string([self])
