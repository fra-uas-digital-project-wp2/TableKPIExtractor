# ============================================================================================================================
# PDF_Analyzer
# File   : AnalyzerCluster.py
# Author : Ismail Demir (G124272)
# Date   : 21.07.2020
#
# Note   : 1 AnalyzerPage refers to * AnalyzerCluster (for the root-node of each cluster)
# ============================================================================================================================

from Format_Analyzer import Format_Analyzer
from globals import dist, print_verbose
from KPISpecs import KPISpecs
from KPIMeasure import KPIMeasure
from Rect import Rect


class AnalyzerCluster:
    """
    Represents an analyzer cluster that contains methods for finding KPIs within the cluster.

    Attributes:
        html_cluster (HTMLCluster): The HTML cluster associated with the analyzer cluster.
        html_page (HTMLPage): The HTML page containing the items.
        items (list): List of HTML items in the HTML page.
        default_year: The default year value.
        bad_page (bool): Indicates if the page is considered bad.

    Methods:
        find_kpis_single_node(kpi_specs, cluster): Finds KPIs within a single cluster node.
        find_kpis_rec(kpi_specs, cluster): Recursively finds KPIs within the cluster.
        find_kpis(kpi_specs): Finds KPIs within the entire HTML cluster.
    """
    html_cluster = None
    html_page = None
    items = None
    default_year = None
    bad_page = None

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

    def find_kpis_single_node(self, kpi_specs, cluster):
        """
        Finds KPIs within a single cluster node.
        Args:
            kpi_specs (KPISpecs): The KPI specifications.
            cluster (HTMLCluster): The HTML cluster.
        Returns:
            KPIMeasure or None: The KPI measure if found, otherwise None.
        """

        def get_txt_by_idx_list(idx_list):
            res = ''
            for idx in idx_list:
                if res != '':
                    res += ', '
                res += self.items[idx].txt
            return res

        def get_rect_by_idx_list(idx_list):
            rect = Rect(9999999, 9999999, -1, -1)
            for idx in idx_list:
                rect.grow(self.items[idx].get_rect())
            return rect

        def refine_txt_items(idx_list, base_score):
            needed = []
            for i in range(len(idx_list)):
                sub_idx_list = idx_list[0:i] + idx_list[i + 1:len(idx_list)]
                sub_txt = get_txt_by_idx_list(sub_idx_list)
                txt_match, score = kpi_specs.match_nodes([sub_txt])
                if score >= base_score and txt_match:
                    needed.append(False)
                else:
                    needed.append(True)
            res = []
            for i in range(len(idx_list)):
                if needed[i]:
                    res.append(idx_list[i])
            return res

        def find_nearest_matching_str(idx_list, ref_point_x, ref_point_y, matching_fun, exclude_years):
            best = -1
            best_word = -1
            best_dist = 9999999
            best_rect = None

            for i in range(len(idx_list)):
                it = self.items[idx_list[i]]
                txt = it.txt if not exclude_years else Format_Analyzer.exclude_all_years(it.txt)
                print_verbose(7, '-------->Looking for ' + str(matching_fun) + ' in: "' + txt + '"')
                if matching_fun(txt):
                    # whole string
                    print_verbose(7, '----------> FOUND!')
                    cur_x, cur_y = it.get_rect().get_center()
                    cur_dist = dist(ref_point_x, ref_point_y, cur_x, cur_y)
                    if cur_dist < best_dist:
                        best_dist = cur_dist
                        best = i
                        best_word = -1
                        best_rect = it.get_rect()
                else:
                    # each word
                    for j in range(len(it.words)):
                        wtxt = it.words[j].txt if not exclude_years else Format_Analyzer.exclude_all_years(
                            it.words[j].txt)
                        print_verbose(7, '-------->Looking for ' + str(matching_fun) + ' in: "' + wtxt + '"')
                        if matching_fun(wtxt):
                            print_verbose(7, '----------> FOUND!')
                            cur_x, cur_y = it.words[j].rect.get_center()
                            cur_dist = dist(ref_point_x, ref_point_y, cur_x, cur_y)
                            if cur_dist < best_dist:
                                best_dist = cur_dist
                                best = i
                                best_word = j
                                best_rect = it.words[j].rect

            if best == -1:
                return None, None, best_rect

            if best_word == -1:
                return idx_list[best], self.items[idx_list[best]].txt, best_rect

            return idx_list[best], self.items[idx_list[best]].words[best_word].txt, best_rect

        print_verbose(5, 'ANALYZING CLUSTER NODE ===>>> ' + cluster.flat_text)

        txt = cluster.flat_text

        idx_list = cluster.get_idx_list()

        # get text

        txt_match, score = kpi_specs.match_nodes([txt])
        print_verbose(5, '---> txt base_score=' + str(score))
        if not txt_match:
            print_verbose(5, '---> No match')
            return None

        idx_list_refined_txt = refine_txt_items(idx_list, score)
        txt_refined = get_txt_by_idx_list(idx_list_refined_txt)

        txt_match, score = kpi_specs.match_nodes([txt_refined])
        print_verbose(5, '------> After refinement: ' + txt_refined)
        print_verbose(5, '------> txt score=' + str(score))

        base_point_x, base_point_y = get_rect_by_idx_list(idx_list_refined_txt).get_center()

        # get value

        raw_value_idx, raw_value, value_rect = find_nearest_matching_str(idx_list, base_point_x, base_point_y,
                                                                         kpi_specs.match_value,
                                                                         not kpi_specs.value_must_be_year)  # TODO: Maybe not always exclude years ?
        if raw_value is None:
            print_verbose(5, '---> Value missmatch')
            return None  # value missmatch

        print_verbose(5, '------> raw_value: ' + str(raw_value))

        # get unit
        txt_unit_matched = kpi_specs.match_unit(txt)
        if not txt_unit_matched:
            print_verbose(5, '---> Unit not matched')
            return None  # unit not matched

        unit_str = ''
        unit_idx = None
        if kpi_specs.has_unit():
            unit_idx, unit_str, foo = find_nearest_matching_str(idx_list, base_point_x, base_point_y,
                                                                kpi_specs.match_unit,
                                                                True)  # TODO: Maybe not always exclude years ?
            if unit_idx is None:
                print_verbose(5, '---> Unit not matched in individual item')
                return None

        print_verbose(5, '------> unit_str: ' + str(unit_str))

        # get year
        year = -1
        year_idx, year_str, foo = find_nearest_matching_str(idx_list, base_point_x, base_point_y,
                                                            Format_Analyzer.looks_year, False)
        if year_str is not None:
            year = Format_Analyzer.to_year(year_str)

        print_verbose(5, '------> year_str: ' + str(year_str))

        # get new idx list
        base_new_idx_list = idx_list_refined_txt
        base_new_idx_list.append(raw_value_idx)
        if unit_idx is not None:
            base_new_idx_list.append(unit_idx)
        if year_idx is not None:
            base_new_idx_list.append(year_idx)

        base_rect = Rect(9999999, 9999999, -1, -1)
        for idx in base_new_idx_list:
            print_verbose(7, '................----> base_item=' + str(self.items[idx]))
            base_rect.grow(self.items[idx].get_rect())

        print_verbose(5, '----> base_rect=' + str(base_rect))

        new_idx_list_in_rect = self.html_page.find_items_within_rect_all_categories(base_rect)
        new_idx_list = list(set.intersection(set(new_idx_list_in_rect), set(idx_list)))

        final_txt = get_txt_by_idx_list(new_idx_list)
        print_verbose(5, '------> Final text: "' + str(final_txt) + '"')

        txt_match, final_txt_score = kpi_specs.match_nodes([final_txt])
        print_verbose(5, '---> txt final_score=' + str(final_txt_score))
        if not txt_match:
            print_verbose(5, '---> No match')
            return None

        rect = Rect(9999999, 9999999, -1, -1)
        anywhere_match_score = 9999999
        for idx in new_idx_list:
            rect.grow(self.items[idx].get_rect())
            anywhere_match, anywhere_match_score_cur = kpi_specs.match_anywhere_on_page(self.html_page, idx)
            anywhere_match_score = min(anywhere_match_score, anywhere_match_score_cur)
            if not anywhere_match:
                print_verbose(5, '---> anywhere-match was not matched on this page. No other match possible.')
                self.bad_page = True
                return None

        kpi_measure = KPIMeasure()
        kpi_measure.kpi_id = kpi_specs.kpi_id
        kpi_measure.kpi_name = kpi_specs.kpi_name
        kpi_measure.src_file = 'TODO'
        kpi_measure.page_num = self.html_page.items[raw_value_idx].page_num
        kpi_measure.item_ids = idx_list
        kpi_measure.pos_x = value_rect.x0  # (rect.x0+rect.x1)*0.5
        kpi_measure.pos_y = value_rect.y0  # (rect.y0+rect.y1)*0.5
        kpi_measure.raw_txt = raw_value
        kpi_measure.year = year
        kpi_measure.value = kpi_specs.extract_value(raw_value)
        kpi_measure.score = final_txt_score + anywhere_match_score
        kpi_measure.unit = unit_str
        kpi_measure.match_type = 'AC.default'
        print_verbose(5, '---> Match: ' + str(kpi_measure) + ': final_txt_score=' + str(
            final_txt_score) + ',anywhere_match_score=' + str(anywhere_match_score))

        return kpi_measure

    def find_kpis_rec(self, kpi_specs, cluster):
        """
        Recursively finds KPIs within the cluster.
        Args:
            kpi_specs (KPISpecs): The KPI specifications.
            cluster (HTMLCluster): The HTML cluster.
        Returns:
            list: List of KPI measures found within the cluster.
        """
        cur_kpi = self.find_kpis_single_node(kpi_specs, cluster)

        res = []
        if cur_kpi is not None:
            res = [cur_kpi]

        for c in cluster.children:
            res.extend(self.find_kpis_rec(kpi_specs, c))

        return res

    def find_kpis(self, kpi_specs):
        """
        Finds KPIs within the entire HTML cluster.
        Args:
            kpi_specs (KPISpecs): The KPI specifications.
        Returns:
            list: List of KPI measures found within the HTML cluster.
        """
        if self.html_cluster is None:
            return []

        res = self.find_kpis_rec(kpi_specs, self.html_cluster)
        return res
