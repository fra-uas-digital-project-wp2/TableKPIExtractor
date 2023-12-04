# ============================================================================================================================
# PDF_Analyzer
# File   : ConsoleTable.py
# Author : Ismail Demir (G124272)
# Date   : 20.07.2020
# ============================================================================================================================


class ConsoleTable:
    """Class for creating and formatting tables for console output."""

    # Class constants
    FORMAT_NICE_CONSOLE = 0
    FORMAT_CSV = 1

    def __init__(self, num_cols):
        """Initialize the ConsoleTable with a specified number of columns."""
        self.num_cols = num_cols
        self.cells = []

    def get_num_rows(self):
        """Calculate and return the number of rows in the table."""
        return int(len(self.cells) / self.num_cols)

    def get(self, row, col):
        """Get the content of a cell at the specified row and column."""
        return self.cells[col + row * self.num_cols]

    def get_native_col_width(self, col):
        """Calculate and return the native width of column based on its content."""
        max_width = 0
        for i in range(self.get_num_rows()):
            max_width = max(max_width, len(self.get(i, col)))
        return max_width

    def to_string(self, max_width=None, min_col_width=None, use_format=FORMAT_NICE_CONSOLE):
        """Convert the table to a string representation with formatting options."""
        if use_format == ConsoleTable.FORMAT_NICE_CONSOLE:
            return self._to_nice_console_string(max_width, min_col_width)
        elif use_format == ConsoleTable.FORMAT_CSV:
            return self._to_csv_string()
        else:
            return 'Unknown format for ConsoleTable\n'

    def _to_nice_console_string(self, max_width, min_col_width):
        """Convert the table to a nice console format."""
        cols = []
        for j in range(self.num_cols):
            cols.append(self.get_native_col_width(j))

        max_col_width = max_width
        while True:
            total_width = 1
            for j in range(self.num_cols):
                total_width += 1 + min(max_col_width, cols[j])
            if total_width <= max_width:
                break
            if max_col_width <= min_col_width:
                break
            max_col_width -= 1

        for j in range(self.num_cols):
            cols[j] = min(max_col_width, cols[j])
        res = ''

        # headline
        res += '\u2554'
        for j in range(self.num_cols):
            res += '\u2550' * cols[j]
            res += '\u2566' if j < self.num_cols - 1 else '\u2557\n'

        # content
        for i in range(self.get_num_rows()):
            # frame line
            if i > 0:
                res += '\u2560'
                for j in range(self.num_cols):
                    res += '\u2550' * cols[j]
                    res += '\u256c' if j < self.num_cols - 1 else '\u2563'
                res += '\n'

            # content line
            res += '\u2551'
            for j in range(self.num_cols):
                txt = self.get(i, j).replace('\n', ' ')
                res += str(txt)[:cols[j]].ljust(cols[j], ' ')
                res += '\u2551'
            res += '\n'

        # footer line
        res += '\u255a'
        for j in range(self.num_cols):
            res += '\u2550' * cols[j]
            res += '\u2569' if j < self.num_cols - 1 else '\u255d\n'
        return res

    def _to_csv_string(self):
        res = ''
        # content
        for i in range(self.get_num_rows()):
            # content line
            for j in range(self.num_cols):
                if j > 0:
                    res += ','
                res += '"' + self.get(i, j).replace('\n', ' ').replace('"', '') + '"'
            res += '\n'
        return res
