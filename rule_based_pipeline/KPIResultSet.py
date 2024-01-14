# ============================================================================================================================
# PDF_Analyzer
# File   : KPIResultSet.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================
import csv
import jsonpickle
from ConsoleTable import ConsoleTable
from KPIMeasure import KPIMeasure


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
            console_table.cells.extend(
                [str(k.kpi_id), str(k.kpi_name), str(k.src_file), str(k.page_num), str(k.item_ids), str(k.pos_x),
                 str(k.pos_y), str(k.raw_txt), str(k.year), str(k.value), str(k.score), str(k.unit), str(k.match_type)]
            )

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

    @staticmethod
    def load_from_csv(csv_file):
        """
        Load a KPIResultSet from a CSV file.

        Args:
            csv_file (str): Path to the CSV file.

        Returns:
            KPIResultSet: The loaded KPIResultSet.
        """
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
        print(data)
        return KPIResultSet.create_from_csv_data(data)

    @classmethod
    def create_from_csv_data(cls, csv_data):
        """
        Create a KPIResultSet instance from CSV data.

        Args:
            csv_data (list): List containing dictionaries with CSV data for each row.

        Returns:
            KPIResultSet: The created KPIResultSet instance.
        """
        kpi_measures = []
        for row in csv_data:
            kpi_measure = KPIMeasure()
            kpi_measure.kpi_id = row["KPI_ID"]
            kpi_measure.kpi_name = row["KPI_NAME"]
            kpi_measure.src_file = row["SRC_FILE"]
            kpi_measure.page_num = row["PAGE_NUM"]
            kpi_measure.item_ids = row["ITEM_IDS"]
            kpi_measure.pos_x = row["POS_X"]
            kpi_measure.pos_y = row["POS_Y"]
            kpi_measure.raw_txt = row["RAW_TXT"]
            kpi_measure.year = row["YEAR"]
            kpi_measure.value = row["VALUE"]
            kpi_measure.score = row["SCORE"]
            kpi_measure.unit = row["UNIT"]
            kpi_measure.match_type = row["MATCH_TYPE"]
            kpi_measures.append(kpi_measure)

        return cls(kpi_measures)

    def __repr__(self):
        """
        String representation of the KPIResultSet.

        Returns:
            str: String representation.
        """
        return self.to_string(120, 5)
