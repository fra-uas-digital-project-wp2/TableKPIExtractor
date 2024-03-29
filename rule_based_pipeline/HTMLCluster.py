# ============================================================================================================================
# PDF_Analyzer
# File   : HTMLCluster.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
#
# Note   : 1 HTMLPage consists of 1 HTMLCluster (root-node)
# Note   : 1 HTMLCluster contains * HTMLClusters (internal nodes), or consists of 1 HTMLItem (leaf node)
# ============================================================================================================================
import numpy
import scipy.cluster.hierarchy as hcl
from globals import hsv_to_rgba, dist, print_verbose
from scipy.spatial.distance import squareform

CLUSTER_DISTANCE_MODE_EUCLIDIAN = 0
CLUSTER_DISTANCE_MODE_RAW_TEXT = 1


class HTMLCluster:
    """
    Represents a cluster in an HTML context.

    Attributes:
        idx (int): The index of the cluster.
        children (list): List of child clusters or items.
        items (list): List of items in the cluster (used internally).
        flat_text (str): The concatenated text of items within the cluster (used internally).
    """

    def __init__(self):
        """
        Initializes an instance of the HTMLCluster class.

        The instance variables are initialized with default or empty values.
        """
        self.idx = -1
        self.children = []
        self.items = []
        self.flat_text = ""

    def is_internal_node(self):
        """
        Check if the cluster is an internal node.

        Returns:
            bool: True if the cluster is an internal node, False otherwise.
        """
        return len(self.children) > 0

    def is_leaf(self):
        """
        Check if the cluster is a leaf node.

        Returns:
            bool: True if the cluster is a leaf node, False otherwise.
        """
        return self.idx != -1

    def calc_flat_text(self):
        """
        Calculate the concatenated text of items within the cluster.
        """
        if self.is_leaf():
            self.flat_text = str(self.items[self.idx].txt)
            return
        first = True
        res = ""
        for c in self.children:
            if not first:
                res += ", "
            c.calc_flat_text()
            res += c.flat_text
            first = False
        self.flat_text = res

    def get_idx_list(self):
        """
        Get a list of indices of items within the cluster.

        Returns:
            list: List of indices.
        """
        if self.is_leaf():
            return [self.idx]

        res = []
        for c in self.children:
            res.extend(c.get_idx_list())
        return res

    def set_items_rec(self, items):
        """
        Set the items list recursively for the cluster.

        Args:
            items (list): List of items.
        """
        self.items = items
        for c in self.children:
            c.set_items_rec(items)

    def count_items(self):
        """
        Count the number of items within the cluster.

        Returns:
            int: Number of items.
        """
        if self.is_leaf():
            return 1
        res = 0
        for c in self.children:
            res += c.count_items()
        return res

    def generate_rendering_colors_rec(self, h0=0.0, h1=0.75):  # h = hue in [0,1]
        """
        Generate rendering colors recursively for items within the cluster.

        Args:
            h0 (float): Starting hue value.
            h1 (float): Ending hue value.
        """
        if self.is_leaf():
            self.items[self.idx].rendering_color = hsv_to_rgba((h0 + h1) * 0.5, 1, 1)
        else:
            num_items_per_child = []
            num_items_tot = 0
            for c in self.children:
                cur_num = c.count_items()
                num_items_per_child.append(cur_num)
                num_items_tot += cur_num
            num_items_acc = 0
            for i in range(len(self.children)):
                self.children[i].generate_rendering_colors_rec(h0 + (h1 - h0) * (num_items_acc / num_items_tot),
                                                               h0 + (h1 - h0) * ((num_items_acc + num_items_per_child[
                                                                   i]) / num_items_tot))
                num_items_acc += num_items_per_child[i]

    def regenerate_not_exported(self, items):
        """
        Regenerate the items list and flat text for the cluster.

        Args:
            items (list): List of items.
        """
        self.set_items_rec(items)
        self.calc_flat_text()

    def cleanup_for_export(self):
        """
        Cleanup internal attributes not needed for export.
        """
        self.items = None
        self.flat_text = None
        for c in self.children:
            c.cleanup_for_export()

    def __repr__(self):
        """
        Return a string representation of the HTMLCluster object.

        Examples:
            "<HTMLItem: line_num=1, pos_x=10.0, pos_y=20.0, is_bold=False, width=100.0, height=30.0, init_height=30.0,
             align=L, brightness=255, cat=0, tmp_ass=0, depth=9990, font_size=12.0, txt='Example Text', id=123,
             pid=-1, nid=124>"

            "<HTMLCluster: <HTMLItem: ...>, <HTMLItem: ...>>"
        """
        if self.is_leaf():
            return str(self.items[self.idx])
        res = "<"
        first = True
        for c in self.children:
            if not first:
                res += ", "
            res += str(c)
            first = False
        res += ">"
        return res

    @staticmethod
    def item_dist(it1, it2, mode):
        """
        Calculate the distance between two items based on the specified mode.

        Args:
            it1: First item.
            it2: Second item.
            mode (int): Distance calculation mode.

        Returns:
            float: Distance between the items.
        """
        if mode == CLUSTER_DISTANCE_MODE_EUCLIDIAN:
            it1_x, it1_y = it1.get_rect().get_center()
            it2_x, it2_y = it2.get_rect().get_center()
            return dist(it1_x, it1_y, it2_x, it2_y)
        elif mode == CLUSTER_DISTANCE_MODE_RAW_TEXT:
            return dist(0, it1.pos_y, 0, it2.pos_y)
        # return dist(it1.pos_x * 100, it1.pos_y, it2.pos_x * 100, it2.pos_y) #TODO: Add this a a new distance mode ! (20.09.2022)

        raise ValueError('Invalid distance mode')

    @staticmethod
    def generate_clusters(items, mode):
        """
        Generate hierarchical / agglomerative clusters from a list of HTMLItems.
        The HTMLItems are added to a "nodes" list.
        The distance between all elements of nodes is calculated.
        A cluster is generated through hierarchical clustering.

        Args:
            items (list): LHTMLItems.
            mode (int): Distance calculation mode.

        Returns:
            HTMLCluster: The root cluster node.
        """
        print_verbose(3, "Regenerating clusters")

        if len(items) < 2:
            return None

        # generate a leaf for each item
        nodes = []

        for it in items:
            cur = HTMLCluster()
            cur.items = items
            cur.idx = it.this_id
            nodes.append(cur)

        print_verbose(3, 'Leaves: ' + str(nodes))

        # generate distance matrix
        l = len(items)
        dmatrix = numpy.zeros((l, l))
        for i in range(l):
            for j in range(i + 1, l):
                d = HTMLCluster.item_dist(items[i], items[j], mode)
                dmatrix[i, j] = d
                dmatrix[j, i] = d

        print_verbose(5, dmatrix)

        # Compute agglomerative cluster, from distance matrix
        sq = squareform(dmatrix)
        output_linkage = hcl.linkage(sq, method='average')

        # build up tree
        num_rows = numpy.size(output_linkage, 0)
        print_verbose(5, output_linkage)

        for i in range(num_rows):
            cur_cluster = HTMLCluster()
            cur_cluster.children.append(nodes[int(output_linkage[i, 0])])
            cur_cluster.children.append(nodes[int(output_linkage[i, 1])])
            nodes.append(cur_cluster)

        res = nodes[len(nodes) - 1]
        res.regenerate_not_exported(items)

        print_verbose(3, 'Clustering result: ' + str(res))

        return res
