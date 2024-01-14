# ============================================================================================================================
# PDF_Analyzer
# File   : AnalyzerCluster.py
# Author : Ismail Demir (G124272)
# Date   : 21.07.2020
# Note   : 1 AnalyzerPage refers to * AnalyzerCluster (for the root-node of each cluster)
# ============================================================================================================================

# TODO: delete?
class AnalyzerCluster:
    """
    Represents an analyzer cluster.

    Attributes:
        html_cluster (HTMLCluster): The HTML cluster associated with the analyzer cluster.
        html_page (HTMLPage): The HTML page containing the items.
        items (list): List of HTML items in the HTML page.
        default_year: The default year value.
        bad_page (bool): Indicates if the page is considered bad.
    """
    def __init__(self, html_cluster, html_page, default_year):
        """
        Initializes an AnalyzerCluster.

        Args:
            html_cluster (HTMLCluster): The HTML cluster.
            html_page (HTMLPage): The HTML page.
            default_year: The default year value.
        """
        self.html_cluster = html_cluster
        self.html_page = html_page
        self.items = html_page.items
        self.default_year = default_year
        self.bad_page = False
