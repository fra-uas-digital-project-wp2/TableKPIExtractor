# ============================================================================================================================
# PDF_Analyzer
# File   : AnalyzerTable.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 AnalyzerDirectory refers to * AnalyzerPage (one for each HTMLPage in that directory, resp. pdf-file)
# ============================================================================================================================

from AnalyzerPage import AnalyzerPage
from config import global_analyze_multiple_pages_at_one, global_ignore_all_years
from globals import print_verbose
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
    html_directory = None
    analyzer_page = None
    default_year = None

    def __init__(self, html_directory, default_year):
        """
        Initializes an AnalyzerDirectory.

        Args:
            html_directory (HTMLDirectory): The HTML directory.
            default_year: The default year value.
        """
        self.html_directory = html_directory
        self.analyzer_page = []
        for i in range(len(self.html_directory.htmlpages)):
            p = html_directory.htmlpages[i]
            self.analyzer_page.append(AnalyzerPage(p, default_year))
            if global_analyze_multiple_pages_at_one and i < len(self.html_directory.htmlpages) - 1:
                p_mult = HTMLPage.merge(p, html_directory.htmlpages[i + 1])
                self.analyzer_page.append(AnalyzerPage(p_mult, default_year))
        self.default_year = default_year

    def fix_src_name(self, kpi_measures):
        """
        Fixes the source file name for a list of KPI measures.

        Args:
            kpi_measures (list): List of KPI measures.
        Returns:
            list: List of KPI measures with fixed source file names.
        """
        print_verbose(3, "self.html_directory.src_pdf_filename=" + self.html_directory.src_pdf_filename)
        res = []
        for k in kpi_measures:
            k.set_file_path(self.html_directory.src_pdf_filename)
            res.append(k)
        return res

    def find_kpis(self, kpi_specs):
        # find all possible occurrences of kpi on all pages
        """
        Finds KPIs within the entire analyzer directory.

        Args:
            kpi_specs (KPISpecs): The KPI specifications.
        Returns:
            list: List of KPI measures found within the analyzer directory.
        """
        res = []
        for a in self.analyzer_page:
            res.extend(a.find_kpis(kpi_specs))

        if global_ignore_all_years:
            res = KPIMeasure.remove_all_years(res)

        res = KPIMeasure.remove_duplicates(res)
        res = KPIMeasure.remove_bad_scores(res, kpi_specs.minimum_score)
        return res

    def find_multiple_kpis(self, kpi_specs_list):
        """
        Finds multiple KPIs within the entire analyzer directory.

        Args:
            kpi_specs_list (list): List of KPI specifications.

        Returns:
            list: List of KPI measures found within the analyzer directory.
        """
        res = []

        for k in kpi_specs_list:
            res.extend(self.find_kpis(k))

        res = KPIMeasure.remove_bad_years(res, self.default_year)
        res = KPIMeasure.remove_duplicates(res)
        res = self.fix_src_name(res)
        return res
