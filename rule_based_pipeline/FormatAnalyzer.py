# ============================================================================================================================
# PDF_Analyzer
# File   : Format_Analyzer.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================
import re
from globals import remove_bad_chars


class FormatAnalyzer:

    pattern_numeric = re.compile(r'^\(?(-?\(?\s*\d*(,\d{3})*(?:\.\d+)?|-?\s*\d*(\.\d{3})*(,\d+)?)\)?(\*?)*$')

    pattern_year = re.compile(r'^[^0-9]*(19[8-9][0-9](/[0-9][0-9])?|20[0-9][0-9](/[0-9][0-9])?)[^0-9]*$')  # 1980-2099

    pattern_year_extended_1 = re.compile(r'^.*[0-3]\d[./\\][0-3]\d[./\\](?:19[8-9]\d|20\d{2}).*$')

    pattern_year_extended_2 = re.compile(r'^.*(?:19[8-9]\d|20\d{2})[./\\][0-3]\d[./\\][0-3]\d.*$')

    pattern_year_in_txt = re.compile(r'(19[8-9][0-9]|20[0-9][0-9])')  # 1980-2099

    pattern_whitespace = re.compile("^\s+|\s+$")

    pattern_ends_with_full_stop = re.compile(".*\.$")

    pattern_pagenum = re.compile(r'^[0-9]{1,3}$')

    pattern_non_numeric_char = re.compile(r'[^0-9.-]')

    pattern_cleanup_text = re.compile(r'[^a-z ]')

    '''
    pattern_footnote: [0-9]+\).*
        [0-9]+  Match one or more digits.
        \)      Match the closing parenthesis.
        .*      Match any characters after the digits and closing parenthesis.
    '''
    pattern_footnote = re.compile(r'[0-9]+\).*')

    '''
    pattern_file_path: (.*/) (.*) \.(.*)
        (.*/):  Captures the directory portion of the path. 
        (.*):   Captures the filename (excluding the extension).
        \.(.*): Captures the file extension.
    '''
    pattern_file_path = re.compile(r'(.*/)(.*)\.(.*)')

    '''
    pattern_cleanup_filename: [()\[\]]
        Matches any of the specified characters: (, ), [, or ].
    '''
    pattern_cleanup_filename = re.compile(r'[()\[\]]')

    @staticmethod
    def trim_whitespaces(val):
        """
        Remove whitespaces from the given value.

        Args:
            val (str): The input value.

        Returns:
            str: The value with whitespaces removed.
        """
        return re.sub(FormatAnalyzer.pattern_whitespace, '', val)

    @staticmethod
    def looks_numeric(val):
        """
        Check if the given value looks like a numeric value.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a numeric value, False otherwise.
        """
        val0 = remove_bad_chars(val, ' ()$%')
        return FormatAnalyzer.pattern_numeric.match(val0.replace('WLTP', '')) and len(val0) > 0  # by Lei

    @staticmethod
    def looks_weak_numeric(val):
        """
        Returns True if at least on integer is in String.

        Args:
            val (str): String to be investigated.

        Returns:
            boolean: True if at least one integer.
        """
        num_numbers = sum(c.isnumeric() for c in val)
        return num_numbers > 0

    @staticmethod
    def looks_percentage(val):
        """
        Check if the given value looks like a percentage.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a weak numeric and contains '%', False otherwise.
        """
        return FormatAnalyzer.looks_weak_numeric(val) and '%' in val

    @staticmethod
    def to_year(val):
        """
        Convert the given value to a year (integer).

        Args:
            val (str): The input value.

        Returns:
            int: The converted year.
        """
        val0 = re.sub(r'[^0-9]', '', val)
        return int(val0)

    @staticmethod
    def looks_year(val):
        """
        Check if the given value looks like a year.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a year, False otherwise.
        """
        return FormatAnalyzer.pattern_year.match(val.replace(' ', ''))

    @staticmethod
    def looks_year_extended(val):
        """
        Return the year if found in the given value, otherwise return None.

        Args:
            val (str): The input value.

        Returns:
            int or None: The extracted year if found, otherwise None.
        """
        if FormatAnalyzer.pattern_year_extended_1.match(val.replace(' ', '')):
            return int(FormatAnalyzer.pattern_year_extended_1.match(val.replace(' ', '')).groups()[2])
        if FormatAnalyzer.pattern_year_extended_2.match(val.replace(' ', '')):
            return int(FormatAnalyzer.pattern_year_extended_2.match(val.replace(' ', '')).groups()[0])
        if FormatAnalyzer.looks_year(val):
            return FormatAnalyzer.to_year(val)

        return None

    @staticmethod
    def cleanup_number(val):
        """
        Clean up the given value by removing non-numeric characters and filtering out extra dots.

        Args:
            val (str): The input value.

        Returns:
            str: The cleaned-up numeric string.
        """
        s = re.sub(FormatAnalyzer.pattern_non_numeric_char, '', val)
        first_dot = s.find('.')
        if first_dot == -1:
            return s

        return s[0:first_dot + 1] + s[first_dot + 1:].replace('.', '')

    @staticmethod
    def to_int_number(val, limit_chars=None):
        """
        Convert the given value to an integer.

        Args:
            val (str): The input value.
            limit_chars (int, optional): Limit the number of characters considered for conversion.

        Returns:
            int or None: The converted integer or None if conversion fails.
        """
        s = FormatAnalyzer.cleanup_number(val)
        if s == '':
            return None
        return int(float(s if limit_chars is None else s[0:limit_chars]))

    @staticmethod
    def to_float_number(val):
        """
        Convert the given value to a float number.

        Args:
            val (str): The input value.

        Returns:
            float or None: The converted floating-point number or None if conversion fails.
        """
        s = FormatAnalyzer.cleanup_number(val)
        if s == '':
            return None
        return float(s)

    @staticmethod
    def cleanup_text(val):
        """
        Remove all characters except letters and spaces from the given text.

        Args:
            val (str): The input text.

        Returns:
            str: The cleaned-up text.
        """
        return re.sub(FormatAnalyzer.pattern_cleanup_text, '', val)

    @staticmethod
    def looks_words(val):
        """
        Check if the given value looks like a word.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a word, False otherwise.
        """
        num_letters = sum(c.isalpha() for c in val)
        return num_letters > 5

    @staticmethod
    def looks_weak_non_numeric(val):
        """
        Check if the given value looks like a weak non-numeric item.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a weak non-numeric item, False otherwise.
        """
        num_letters = sum(c.isalpha() for c in val)
        num_numbers = sum(c.isnumeric() for c in val)
        num_others = len(val) - (num_letters + num_numbers)

        return (
            num_letters > 0
            and num_letters > num_numbers
            and (
                (num_letters + num_others > 1 and num_numbers < (num_letters + num_others) * 2 + 1)
                or (num_letters + num_others > num_numbers)
            )
        )

    @staticmethod
    def looks_other_special_item(val):
        """
        Check if the given value looks like another special item.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like another special item, False otherwise.
        """
        return len(val) < 4 and not FormatAnalyzer.looks_words(val) and not FormatAnalyzer.looks_numeric(val)

    @staticmethod
    def looks_pagenum(val):
        """
        Check if the given value looks like a page number.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a page number, False otherwise.
        """
        return FormatAnalyzer.pattern_pagenum.match(val.replace(' ', '')) and len(val) > 0 and val.replace(' ', '')

    @staticmethod
    def looks_running_text(val):
        """
        Determines if a string can be classified as a running text.

        Args:
            val (str): String to be investigated.

        Returns:
            Boolean: True if the string to be investigated looks like text.
        """
        txt = FormatAnalyzer.trim_whitespaces(val)
        num_full_stops = txt.count(".")
        num_comma = txt.count(",")
        num_space = txt.count(" ")
        ends_with_full_stop = True if FormatAnalyzer.pattern_ends_with_full_stop.match(txt) else False
        txtlen = len(txt)
        num_letters = sum(c.isalpha() for c in txt)
        if num_letters < 20:
            return False  # too short
        if num_letters / txtlen < 0.5:
            return False  # strange: less than 50% are letters
        if num_space < 5:
            return False  # only 5 words or fewer
        if num_comma / txtlen < 0.004 and num_full_stops / txtlen < 0.002:
            return False  # too few commans / full stops
        if ends_with_full_stop:
            # looks like a sentence
            return True

        # does not end with full stop, so we require more conditions to hold
        return ((num_full_stops > 2) or (num_full_stops > 1 and num_comma > 1)) and (num_letters > 30) and (
                    num_space > 10)

    @staticmethod
    def looks_footnote(val):
        """
        Check if the given value looks like a footnote.

        Args:
            val (str): The input value.

        Returns:
            bool: True if the value looks like a footnote, False otherwise.
        """
        return FormatAnalyzer.pattern_footnote.match(val.replace(' ', '').lower())

    @staticmethod
    def extract_file_name(val):
        """
        Extract the file name from the given value.

        Args:
            val (str): The input value.

        Returns:
            str: Extracted file name.
        """
        fp = FormatAnalyzer.extract_file_path('/' + val.replace('\\', '/'))
        return fp[1] + '.' + fp[2]

    @staticmethod
    def extract_year_from_text(val):
        """
        Extract the year from the given text.

        Args:
            val (str): The input text.

        Returns:
            int or None: Extracted year if found, None otherwise.
        """
        lst = list(set(re.findall(FormatAnalyzer.pattern_year_in_txt, val)))
        if len(lst) == 1:
            return int(lst[0])
        return None

    @staticmethod
    def cnt_overlapping_items(l0, l1):
        """
        Count the number of overlapping items between two lists.

        Args:
            l0 (list): The first list.
            l1 (list): The second list.

        Returns:
            int: Number of overlapping items.
        """
        return len(list(set(l0) & set(l1)))

    @staticmethod
    def extract_file_path(value):
        """
        Extracts file information (path, name and extension of the file) using Format_Analyzer's pattern_file_path.

        Args:
            value (str): The input value containing the file path.

        Returns:
            tuple: A tuple containing the path, name and extension of the extracted file.

        Example: /path/to/file/filename.pdf
            ('/path/to/file/', 'filename', 'pdf')
        """
        return FormatAnalyzer.pattern_file_path.match(value).groups()

    @staticmethod
    def cleanup_filename(value):
        """
        Cleans up a filename by replacing certain characters [, ], (, or ) with underscores.

        Args:
            value (str): The input filename.

        Returns:
            str: The cleaned filename with specified characters replaced by underscores.

        Example: filename[12]test
                -> filename_12_test
        """
        return re.sub(FormatAnalyzer.pattern_cleanup_filename, '_', value)
