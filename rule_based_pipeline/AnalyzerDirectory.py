# ============================================================================================================================
# PDF_Analyzer
# File   : AnalyzerTable.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 AnalyzerDirectory refers to * AnalyzerPage (one for each HTMLPage in that directory, resp. pdf-file)
# ============================================================================================================================
from AnalyzerPage import AnalyzerPage
from config_for_rb import global_analyze_multiple_pages_at_one, global_ignore_all_years
from HTMLDirectory import HTMLDirectory
from HTMLPage import HTMLPage
from KPIMeasure import KPIMeasure


class AnalyzerDirectory:
    """
    Represents an analyzer directory that contains methods for finding KPIs within the directory.

    Attributes:
        html_directory (HTMLDirectory): The HTML directory associated with the analyzer directory.
        analyzer_page (list): List of AnalyzerPage objects for each HTML page in the directory.
        default_year: The default year value.

    Methods:
        fix_src_name(kpi_measures): Fixes the source file name for a list of KPI measures.
        find_kpis(kpi_specs): Finds KPIs within the entire analyzer directory.
        find_multiple_kpis(kpi_specs_list): Finds multiple KPIs within the entire analyzer directory.
    """

    def __init__(self, html_directory, default_year):
        """
        Initializes an AnalyzerDirectory.

        Args:
            html_directory (HTMLDirectory): The HTMLDirectory (Report).
            default_year: The default year value.
        """
        self.html_directory = html_directory
        self.analyzer_page = []
        self.default_year = default_year

        # Create AnalyzerPage objects for each HTML page in the directory
        for i in range(len(self.html_directory.htmlpages)):
            page = html_directory.htmlpages[i]
            self.analyzer_page.append(AnalyzerPage(page, default_year))

            # Merge consecutive pages if specified
            if global_analyze_multiple_pages_at_one and i < len(self.html_directory.htmlpages) - 1:
                multiple_pages = HTMLPage.merge(page, html_directory.htmlpages[i + 1])
                self.analyzer_page.append(AnalyzerPage(multiple_pages, default_year))

    def fix_src_name(self, kpi_measures):
        """
        Fixes the source file name for a list of KPI measures.

        Args:
            kpi_measures (list): List of KPI measures.
        Returns:
            list: List of KPI measures with fixed source file names.
        """
        result = []

        # Iterate through each KPI measure and set the source file name
        for kpi_measure in kpi_measures:
            kpi_measure.set_file_path(self.html_directory.src_pdf_filename)
            result.append(kpi_measure)

        return result

    def find_kpis(self, kpi_specs):
        """
        Finds KPIs within the entire analyzer directory.

        Args:
            kpi_specs (KPISpecs): The KPI specifications.
        Returns:
            list: List of KPI measures found within the analyzer directory.
        """
        result = []

        # Iterate through each AnalyzerPage and find KPIs
        for page in self.analyzer_page:
            result.extend(page.find_kpis(kpi_specs))

        # Remove all years if specified
        if global_ignore_all_years:
            result = KPIMeasure.remove_all_years(result)

        # Remove duplicate KPI measures and those with scores below the minimum
        result = KPIMeasure.remove_duplicates(result)
        result = KPIMeasure.remove_bad_scores(result, kpi_specs.minimum_score)

        return result

    def find_multiple_kpis(self, kpi_specs_list):
        """
        Finds multiple KPIs within the entire analyzer directory.

        Args:
            kpi_specs_list (list): List of KPI specifications.

        Returns:
            list: List of KPI measures found within the analyzer directory.
        """

        result = []

        # Iterate through each KPI specification and find KPIs
        for kpi_spec in kpi_specs_list:
            result.extend(self.find_kpis(kpi_spec))

        # Remove KPIs with bad years, duplicates, and fix source file names
        result = KPIMeasure.remove_bad_years(result, self.default_year)
        result = KPIMeasure.remove_duplicates(result)
        result = self.fix_src_name(result)

        return result
