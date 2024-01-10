# ============================================================================================================================
# PDF_Analyzer
# File   : AnalyzerPage.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 AnalyzerPage refers to * AnalyzerTable (one for each HTMLTable on that page)
# Note   : 1 AnalyzerDirectory refers to * AnalyzerPage (one for each HTMLPage in that directory, resp. pdf-file)
# ============================================================================================================================
from HTMLPage import HTMLPage
from AnalyzerTable import AnalyzerTable
from AnalyzerCluster import AnalyzerCluster
from KPIMeasure import KPIMeasure
from globals import print_verbose


class AnalyzerPage:
    """
    Represents an analyzer page that contains methods for finding KPIs within the page.

    Attributes:
        html_page (HTMLPage): The HTML page associated with the analyzer page.
        analyzer_table (list): List of AnalyzerTable objects for each HTML table in the page.
        analyzer_cluster (list): List of AnalyzerCluster objects for each cluster in the page.
        default_year: The default year value.
    Methods:
        find_kpis(kpi_specs): Finds KPIs within the analyzer page.
    """
    def __init__(self, html_page, default_year):
        """
        Initializes an AnalyzerPage.

        Args:
            html_page (HTMLPage): The HTML page.
            default_year: The default year value.
        """
        self.html_page = html_page

        self.analyzer_table = []
        for table in self.html_page.tables:
            self.analyzer_table.append(AnalyzerTable(table, self.html_page, default_year))
            sub_tabs = table.generate_sub_tables()
            for sub_tab in sub_tabs:
                self.analyzer_table.append(AnalyzerTable(sub_tab, self.html_page, default_year))

        self.analyzer_cluster = []
        self.analyzer_cluster.append(AnalyzerCluster(html_page.clusters_text, html_page, default_year))

        self.default_year = default_year

    def find_kpis(self, kpi_specs):
        """
        Finds all KPIs within the analyzer page.

        Args:
            kpi_specs (KPISpecs): The KPI specifications.
        Returns:
            list: List of KPI measures found within the analyzer page.
        """
        print_verbose(1, " ==>>>> FIND KPIS '" + kpi_specs.kpi_name + "' ON PAGE: " + str(
            self.html_page.page_num) + " <<<<<=====")

        result = []
        # 1. Tables
        for table in self.analyzer_table:
            result.extend(table.find_kpis(kpi_specs))

        # 2. Remove duplicates
        result = KPIMeasure.remove_duplicates(result)

        # 3. Adjust coordinates
        for k in result:
            px, py = self.html_page.transform_coords(k.pos_x, k.pos_y)
            k.pos_x = px
            k.pos_y = py

        return result
