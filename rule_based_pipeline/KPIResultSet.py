# ============================================================================================================================
# PDF_Analyzer
# File   : KPIResultSet.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable
import jsonpickle


class KPIResultSet:
    """
    Represents a set of Key Performance Indicators (KPIs) with their measures.
    """

    def __init__(self, kpi_measures=None):
        """
        Initialize a KPIResultSet instance.

        Args:
            kpi_measures (list): A list of KPIMeasure instances.
        """
        if kpi_measures is None:
            kpi_measures = []
        self.kpi_measures = kpi_measures

    def extend(self, kpi_result_set):
        """
        Extend the current KPIResultSet with another KPIResultSet.

        Args:
            kpi_result_set (KPIResultSet): Another KPIResultSet to extend with.
        """
        self.kpi_measures.extend(kpi_result_set.kpi_measures)

    def to_console_table(self):
        """
        Convert the KPIResultSet to a ConsoleTable.

        Returns:
            ConsoleTable: The ConsoleTable representation of the KPIResultSet.
        """
        console_table = ConsoleTable(13)
        # Add header cells
        header_cells = ['KPI_ID', 'KPI_NAME', 'SRC_FILE', 'PAGE_NUM', 'ITEM_IDS', 'POS_X', 'POS_Y', 'RAW_TXT',
                        'YEAR', 'VALUE', 'SCORE', 'UNIT', 'MATCH_TYPE']
        console_table.cells.extend(header_cells)

        # Add data cells
        for k in self.kpi_measures:
            console_table.cells.extend([str(k.kpi_id), str(k.kpi_name), str(k.src_file), str(k.page_num), str(k.item_ids),
                              str(k.pos_x), str(k.pos_y), str(k.raw_txt), str(k.year), str(k.value), str(k.score),
                              str(k.unit), str(k.match_type)])

        return console_table

    def to_string(self, max_width, min_col_width):
        """
        Convert the KPIResultSet to a string representation.

        Args:
            max_width (int): Maximum width of the output string.
            min_col_width (int): Minimum width of each column.

        Returns:
            str: The string representation of the KPIResultSet.
        """
        console_table = self.to_console_table()
        return console_table.to_string(max_width, min_col_width)

    def to_json(self):
        """
        Convert the KPIResultSet to a JSON-formatted string.

        Returns:
            str: The JSON-formatted string representation of the KPIResultSet.
        """
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        data = jsonpickle.encode(self)
        return data

    def save_to_file(self, json_file):
        """
        Save the KPIResultSet to a JSON file.

        Args:
            json_file (str): The path to the JSON file.
        """
        data = self.to_json()
        with open(json_file, "w") as file:
            file.write(data)

    def save_to_csv_file(self, csv_file):
        """
        Save the KPIResultSet to a CSV file.

        Args:
            csv_file (str): The path to the CSV file.
        """
        console_table = self.to_console_table()
        csv_str = console_table.to_string(use_format=ConsoleTable.FORMAT_CSV)

        with open(csv_file, "w", encoding="utf-8") as file:
            file.write(csv_str)

    @staticmethod
    def load_from_json(data):
        """
        Load a KPIResultSet from a JSON-formatted string.

        Args:
            data (str): JSON-formatted string.

        Returns:
            KPIResultSet: The loaded KPIResultSet.
        """
        obj = jsonpickle.decode(data)
        return obj

    @staticmethod
    def load_from_file(json_file):
        """
        Load a KPIResultSet from a JSON file.

        Args:
            json_file (str): Path to the JSON file.

        Returns:
            KPIResultSet: The loaded KPIResultSet.
        """
        with open(json_file, "r") as f:
            data = f.read()
        return KPIResultSet.load_from_json(data)

    def __repr__(self):
        """
        String representation of the KPIResultSet.

        Returns:
            str: String representation.
        """
        return self.to_string(120, 5)
