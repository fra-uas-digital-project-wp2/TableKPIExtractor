# ============================================================================================================================
# PDF_Analyzer
# File   : KPISpecs.py
# Author : Ismail Demir (G124272)
# Date   : 23.06.2020
# ============================================================================================================================
from Format_Analyzer import Format_Analyzer
from globals import print_verbose
import re
from Rect import Rect

# Matching modes:
MATCHING_MUST_INCLUDE = 0  # no match, if not included
MATCHING_MUST_INCLUDE_EACH_NODE = 4  # must be included in each node, otherwise no match. Note: this is even more strict than MATCHING_MUST_INCLUDE

MATCHING_MAY_INCLUDE = 1  # should be included, but inclusion is not necessary, although AT LEAST ONE such item must be included. can also have a negative score
MATCHING_CAN_INCLUDE = 2  # should be included, but inclusion is not necessary. can also have a negative score
MATCHING_MUST_EXCLUDE = 3  # no match, if included

# Distance modes
DISTANCE_EUCLIDIAN = 0  # euclidian distance
DISTANCE_MOD_EUCLID = 1  # euclidian distance, but with modification such that orthogonal aligned objects are given a smaller distance (thus preferring table-like alignments)
DISTANCE_MOD_EUCLID_UP_LEFT = 2  # like 1, but we prefer looking upwards and to the left, which conforms to the typical structure of a table
DISTANCE_MOD_EUCLID_UP_ONLY = 3  # like 1, but we strictly enforce only looking upwards (else, score=0)

# Percentage Matching
VALUE_PERCENTAGE_DONT_CARE = 0
VALUE_PERCENTAGE_MUST = 1
VALUE_PERCENTAGE_MUST_NOT = 2


class KPISpecs:
    # This class contains specifications for one KPI that should be extracted

    # regex matcher for description of KPI
    class DescRegExMatch:
        pattern_raw = None
        pattern_regex = None
        # score must always be > 0
        score = None
        matching_mode = None
        # score_decay should be between 0 and 1. It determines how fast the score decays, when we traverse into more
        # distant nodes. 1=No decay, 0=Full decay after first node
        score_decay = None
        case_sensitive = None
        # If a pattern is hit multiple times, the score will decay after each hit. 1=No decay, 0=Full decay after first node
        multi_match_decay = None
        # Generally, we prefer shorter texts to longer ones, because they contain less distractive garbage. So for each
        # letter, the score decays. 1=No decay, 0 =Immediate, full decay
        letter_decay = None
        # this number of letters will not be affected by decay at all
        letter_decay_disregard = None
        # if this is TRUE (default), then a match will be counted, in cases where a single match is needed
        count_if_matched = None
        # if this is TRUE, then we will try to match against a concatenation of all nodes. Default: FALSE
        allow_matching_against_concat_txt = None

        def __init__(self, pattern_raw, score, matching_mode, score_decay, case_sensitive, multi_match_decay,
                     letter_decay_hl, letter_decay_disregard=0, count_if_matched=True,
                     allow_matching_against_concat_txt=False):
            # specify half-life of letter decay! 0 =No decay
            """
            Initialize a DescRegExMatch instance.

            Args:
                pattern_raw (str): Raw regular expression pattern.
                score (float): Score for the match.
                matching_mode (int): Matching mode.
                score_decay (float): Score decay factor.
                case_sensitive (bool): Whether the matching is case-sensitive.
                multi_match_decay (float): Multi-match decay factor.
                letter_decay_hl (float): Half-life of letter decay.
                letter_decay_disregard (int): Number of letters disregarded in decay. default is 0
                count_if_matched (bool): Whether to count the match if matched. default is True
                allow_matching_against_concat_txt (bool): Whether to match against a concatenation of all nodes. default is False
            """
            self.pattern_raw = pattern_raw
            self.score = score
            self.matching_mode = matching_mode
            self.score_decay = score_decay
            self.case_sensitive = case_sensitive
            # if case_sensitive else pattern_raw.lower())
            # Note: using lower-case here would destroy regexp patterns like \S
            self.pattern_regex = re.compile(pattern_raw)
            self.multi_match_decay = multi_match_decay
            self.letter_decay = 0.5 ** (1.0 / letter_decay_hl) if letter_decay_hl > 0 else 1
            self.letter_decay_disregard = letter_decay_disregard
            self.count_if_matched = count_if_matched
            self.allow_matching_against_concat_txt = allow_matching_against_concat_txt

        def match_single_node(self, txt):
            """
            Check if a single node matches the regular expression.

            Args:
                txt (str): Text of the node.

            Returns:
                bool: True if the node matches, False otherwise.
            """
            return bool(self.pattern_regex.match(txt if self.case_sensitive else txt.lower()))

        def match_nodes(self, txt_nodes):
            """
            Check if nodes are matched by the regular expression.

            Args:
                txt_nodes (list): List of text nodes.

            Returns:
                tuple: (bool, float) representing whether there is a match and the calculated score.
            """
            matched = False
            final_score = 0
            num_hits = 0
            concat_match = False
            concat_final_score = 0

            if self.allow_matching_against_concat_txt:
                concat_txt = ' '.join(txt_nodes)
                if self.match_single_node(concat_txt):
                    concat_final_score = self.score * (self.letter_decay ** max(len(Format_Analyzer.cleanup_text(concat_txt)) - self.letter_decay_disregard, 0))
                    concat_match = True

            for i, txt_node in enumerate(txt_nodes):
                if self.match_single_node(txt_node):
                    if self.matching_mode == MATCHING_MUST_EXCLUDE:
                        return False, -1  # we matched something that must not be included
                    matched = True
                    final_score += self.score * (self.score_decay ** i) * (self.multi_match_decay ** num_hits) * (self.letter_decay ** max(len(Format_Analyzer.cleanup_text(txt_node)) - self.letter_decay_disregard, 0))
                    num_hits += 1
                else:
                    if self.matching_mode == MATCHING_MUST_INCLUDE_EACH_NODE and not concat_match:
                        return False, 0

            if self.matching_mode == MATCHING_MUST_INCLUDE and not matched and not concat_match:
                return False, 0  # something must be included was never matched

            return True, max(concat_final_score, final_score)

    class GeneralRegExMatch:
        """
        A regex matcher for the value or unit of a KPI.
        """
        def __init__(self, pattern_raw, case_sensitive):
            """
            Initialize a GeneralRegExMatch instance.

            Args:
                pattern_raw (str): Raw regular expression pattern.
                case_sensitive (bool): Whether the matching is case-sensitive.
            """
            self.pattern_raw = pattern_raw
            self.case_sensitive = case_sensitive
            self.pattern_regex = re.compile(pattern_raw if case_sensitive else pattern_raw.upper())

        def match(self, txt):
            """
            Check if the text matches the regular expression.

            Args:
                txt (str): Text to match.

            Returns:
                bool: True if the text matches, False otherwise.
            """
            return True if self.pattern_regex.match(txt if self.case_sensitive else txt.upper()) else False

    class AnywhereRegExMatch:
        """
        A regex matcher for text anywhere on the page near the KPI.
        """
        general_match = None
        distance_mode = None
        score = None  # must always be > 0
        matching_mode = None
        score_decay = None  # Should be between 0 and 1. It determines how fast the score decays, when we reach more distant items. 1=No decay, 0=Full decay after 1 px
        multi_match_decay = None  # If a pattern is hit multiple times, the score will decay after each hit. 1=No decay, 0=Full decay after first hit
        letter_decay = None  # Generally, we prefer shorter texts to longer ones, because they contain less distractive garbage. So for each letter, the score decays. 1=No decay, 0 =Immediate, full decay
        letter_decay_disregard = None  # this number of letters will not be affected by decay at all

        def __init__(self, general_match, distance_mode, score, matching_mode, score_decay, multi_match_decay,
                     letter_decay_hl, letter_decay_disregard=0):
            """
            Initialize an AnywhereRegExMatch instance.

            Args:
                general_match: An instance of GeneralRegExMatch for the general matching pattern.
                distance_mode (int): The distance mode for matching.
                score (float): The base score for a match.
                matching_mode (int): The matching mode (e.g., MUST_INCLUDE, MUST_EXCLUDE).
                score_decay (float): Score decay factor.
                multi_match_decay (float): Multi-match decay factor.
                letter_decay_hl (float): Half-life for letter decay.
                letter_decay_disregard (int): The number of letters not affected by decay.
            """
            self.general_match = general_match
            self.distance_mode = distance_mode
            self.score = score
            self.matching_mode = matching_mode
            self.score_decay = score_decay
            self.multi_match_decay = multi_match_decay
            self.letter_decay = 0.5 ** (1.0 / letter_decay_hl) if letter_decay_hl > 0 else 1
            self.letter_decay_disregard = letter_decay_disregard

        def calc_distance(self, a, b, threshold):
            """
            Calculate the distance between two points with a penalty factor.

            Args:
                a (tuple): Coordinates of point A.
                b (tuple): Coordinates of point B.
                threshold (float): Threshold value.

            Returns:
                float: Calculated distance.
            """
            if self.distance_mode == DISTANCE_EUCLIDIAN:
                return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
            if self.distance_mode == DISTANCE_MOD_EUCLID:
                penalty = 1
                if a[1] < b[1] - threshold:
                    penalty = 50  # reference_point text below base point
                if a[0] < b[0] - threshold:
                    penalty = 50 if penalty == 1 else 90  # reference_point text right of base point
                dx = abs(b[0] - a[0])
                dy = abs(b[1] - a[1])
                if dx > dy:
                    dx *= 0.01
                else:
                    dy *= 0.01
                return penalty * (dx * dx + dy * dy) ** 0.5
            if self.distance_mode == DISTANCE_MOD_EUCLID_UP_ONLY:
                penalty = 1
                if a[1] < b[1]:
                    return -1  # reference_point text below base point
                if a[0] < b[0] - threshold:
                    penalty = 50 if penalty == 1 else 90  # reference_point text right of base point
                dx = abs(b[0] - a[0])
                dy = abs(b[1] - a[1])
                if dx > dy:
                    dx *= 0.01
                else:
                    dy *= 0.01
                return penalty * (dx * dx + dy * dy) ** 0.5

            return None  # not implemented

        def match(self, html_page, cur_item_idx):
            """
            Match the pattern anywhere on the page near the current item.

            Args:
                html_page: An instance of the HTML page.
                cur_item_idx (int): The index of the current item.

            Returns:
                tuple: A tuple (bool, float) indicating whether there is a match and the final score.
            """
            taken = [False] * len(html_page.items)
            matches = []  # list of (idx, txt, score_base)
            base_rect = html_page.items[cur_item_idx].get_rect()
            base_point = ((base_rect.x0 + base_rect.x1) * 0.5, (base_rect.y0 + base_rect.y1) * 0.5)
            page_diag = (html_page.page_width ** 2 + html_page.page_height ** 2) ** 0.5
            page_threshold = page_diag * 0.0007

            for i in range(len(html_page.items)):
                if taken[i]:
                    continue
                idx_list = html_page.explode_item_by_idx(i)
                # mark as taken
                for j in idx_list:
                    taken[j] = True
                txt = html_page.explode_item(i)
                if self.general_match.match(txt):
                    rect = Rect(9999999, 9999999, -1, -1)
                    for j in idx_list:
                        rect.grow(html_page.items[j].get_rect())
                    reference_point = ((rect.x0 + rect.x1) * 0.5, (rect.y0 + rect.y1) * 0.5)

                    dist = self.calc_distance(base_point, reference_point, page_threshold)
                    if dist == -1:
                        continue
                    dist_exp = dist / (0.1 * page_diag)

                    score_base = self.score * (self.score_decay ** dist_exp) * (self.letter_decay ** max(
                        len(Format_Analyzer.cleanup_text(txt)) - self.letter_decay_disregard, 0))

                    matches.append((i, txt, score_base))

            matches = sorted(matches, key=lambda m: - m[2])  # sort desc by score_base

            if len(matches) > 0:
                print_verbose(8, 'AnywhereRegExMatch.match of item ' + str(
                    html_page.items[cur_item_idx]) + ' matches with: ' + str(matches))

            final_score = 0
            num_hits = 0
            for i in range(len(matches)):
                if self.matching_mode == MATCHING_MUST_EXCLUDE:
                    return False, -1  # we matched something that must not be included

                final_score += matches[i][2] * (self.multi_match_decay ** num_hits)
                num_hits += 1

            if self.matching_mode in (MATCHING_MUST_INCLUDE, MATCHING_MUST_INCLUDE_EACH_NODE) and len(matches) == 0:
                return False, 0  # something must be included was never matched

            return True, final_score

    kpi_id = None
    kpi_name = None
    desc_regex_match_list = None
    value_regex_match_list = None
    unit_regex_match_list = None
    value_must_be_numeric = None
    value_percentage_match = None
    value_must_be_year = None
    anywhere_regex_match_list = None
    minimum_score = None
    minimum_score_desc_regex = None

    def __init__(self):
        self.kpi_id = -1
        self.kpi_name = ''
        self.desc_regex_match_list = []
        self.value_regex_match_list = []
        self.unit_regex_match_list = []
        self.value_must_be_numeric = False
        self.value_must_be_year = False
        self.value_percentage_match = VALUE_PERCENTAGE_DONT_CARE
        self.anywhere_regex_match_list = []
        self.minimum_score = 0
        self.minimum_score_desc_regex = 0

    def has_unit(self):
        return len(self.unit_regex_match_list) > 0

    # check if nodes are matched by this, and if yes return True together with score
    def match_nodes(self, desc_nodes):
        final_score = 0
        at_least_one_match = False
        bad_match = False
        min_score = 0

        for d in self.desc_regex_match_list:
            match, score = d.match_nodes(desc_nodes)
            print_verbose(7, '..... matching "' + d.pattern_raw + '"  => match,score=' + str(match) + ',' + str(score))
            if not match:
                # must included, but not included. or must excluded, but included
                bad_match = True
                min_score = min(min_score, score)

            if (d.matching_mode in (MATCHING_MAY_INCLUDE, MATCHING_MUST_INCLUDE,
                                    MATCHING_MUST_INCLUDE_EACH_NODE) and d.count_if_matched and match and score > 0):
                print_verbose(9, '............. at least one match here!')
                at_least_one_match = True
            final_score += score

        if bad_match:
            return False, min_score  # 0 = if no match, -1 if must-excluded item was matched

        if not at_least_one_match:
            return False, 0

        return final_score >= self.minimum_score_desc_regex and final_score > 0, final_score

    def match_unit(self, unit_str):
        for u in self.unit_regex_match_list:
            if not u.match(unit_str):
                return False
        return True

    # check if extracted value is a match
    def match_value(self, val_str):
        if self.value_must_be_numeric and (val_str == '' or not Format_Analyzer.looks_numeric(val_str)):
            return False

        if self.value_percentage_match == VALUE_PERCENTAGE_MUST:
            if not Format_Analyzer.looks_percentage(val_str):
                return False

        if self.value_percentage_match == VALUE_PERCENTAGE_MUST_NOT:
            if Format_Analyzer.looks_percentage(val_str):
                return False

        if self.value_must_be_year and not Format_Analyzer.looks_year(val_str):
            return False  # this is not a year!

        for v in self.value_regex_match_list:
            if not v.match(val_str):
                return False
        return True

    def match_anywhere_on_page(self, html_page, cur_item_idx):
        if len(self.anywhere_regex_match_list) == 0:
            return True, 0

        final_score = 0
        at_least_one_match = False
        at_least_one_match_needed = False
        bad_match = False
        min_score = 0

        for d in self.anywhere_regex_match_list:
            if d.matching_mode in (MATCHING_MAY_INCLUDE, MATCHING_MUST_INCLUDE):
                at_least_one_match_needed = True

            match, score = d.match(html_page, cur_item_idx)
            print_verbose(7, '..... matching anywhere "' + d.general_match.pattern_raw + '"  => match,score=' + str(
                match) + ',' + str(score))
            if not match:
                # must include, but not included. or must excluded, but included
                bad_match = True
                min_score = min(min_score, score)

            if d.matching_mode in (MATCHING_MAY_INCLUDE, MATCHING_MUST_INCLUDE):
                at_least_one_match = True
            final_score += score

        if bad_match:
            print_verbose(9, '...........  bad_match')
            return False, min_score  # 0 = if no match, -1 if must-excluded item was matched

        if not at_least_one_match and at_least_one_match_needed:
            print_verbose(9, '...........  not at least one needed match found')
            return False, 0

        return final_score > 0, final_score

    @staticmethod
    def extract_value(val_str):
        # for now just return the input
        # converting to standardized numbers could be done here
        return val_str
