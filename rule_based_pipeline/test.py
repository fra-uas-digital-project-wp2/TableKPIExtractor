# ============================================================================================================================
# PDF_Analyzer
# File   : test.py
# Author : Ismail Demir (G124272)
# Date   : 05.08.2020
#
# Note: This file contains procedure used for testing only.
# ============================================================================================================================


from AnalyzerDirectory import *
from TestData import *
from DataImportExport import *
from TestEvaluation import *
from KPISpecs import *


def test(pdf_file, wildcard):
    dir = HTMLDirectory()
    dir.parse_html_directory(get_html_out_dir(pdf_file), r'page' + str(wildcard) + '.html')
    dir.render_to_png(get_html_out_dir(pdf_file), get_html_out_dir(pdf_file))
    dir.save_to_dir(get_html_out_dir(pdf_file))


def test_convert_pdf(pdf_file):
    HTMLDirectory.convert_pdf_to_html(pdf_file)
    dir = HTMLDirectory()
    dir.parse_html_directory(get_html_out_dir(pdf_file), r'page*.html')
    dir.save_to_dir(get_html_out_dir(pdf_file))


def test_load_json(pdf_file, wildcard):
    dir = HTMLDirectory()
    dir.load_from_dir(get_html_out_dir(pdf_file), 'jpage' + str(wildcard) + '.json')
    return dir


def test_print_all_clusters(htmldir):
    for p in htmldir.htmlpages:
        print(p.clusters_text)


#
# Only used for initial testing
def test_prepare_kpispecs():
    def prepare_kpi_6_scope1_direct_total_ghg_emissions():
        # KPI 6 = Scope 1 / Direct total GHGs emissions
        kpi = KPISpecs()
        kpi.kpi_id = 6
        kpi.kpi_name = 'Scope 1 / Direct total GHGs emissions'

        # Match paragraphs
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2).*emissions?.*', score=7000,
            matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gas emissions')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(^|[^a-z])co2.*emissions?.*tCO2e.*', score=10000,
                                    matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('co2 emissions')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw='.*scope[^a-zA-Z0-9]?1.*', score=12000,
                                                                 matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1,
                                                                 case_sensitive=False, multi_match_decay=0,
                                                                 letter_decay_hl=20,
                                                                 letter_decay_disregard=len('scope 1')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2|combustion.*fuels?).*emissions?.*',
            score=7000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gas emissions')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(^|[^a-z])combustion.*fuels?.*', score=6000,
                                    matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.1, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('gas emissions')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*(direct)(emissions?)?.*', score=9000,
            matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=15, letter_decay_disregard=len('gas direct')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*direct.*scope[^a-zA-Z0-9]?1(emissions?)?.*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('direct scope 1')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*direct.*(gas|ghg|(ghg)|atmospheric).*scope[^a-zA-Z0-9]?1(emissions?)?.*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('direct scope 1')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*scope\s1.*', score=6000, matching_mode=MATCHING_MAY_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=30,
                                    letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*direct.*scope[^a-zA-Z0-9]?1(emissions?)?.*m.*t',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*scope[^a-zA-Z0-9]?2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
                                    score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(((gas|ghg|(ghg)|atmospheric)|direct).*emissions?|scope[^a-zA-Z0-9]?1).*(million\s? tonnes|co2[^a-zA-Z0-9]?eq)',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])((gas|ghg|(ghg)|atmospheric)|direct).*(million\s? tonnes|co2[^a-zA-Z0-9]?eq).*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])direct.*(gas|ghg|(ghg)).*(million\s? tonnes|co2[^a-zA-Z0-9]?(eq|equivalent)).*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(scope[^a-zA-Z0-9]?2|scope[^a-zA-Z0-9]?3).*', score=1,
                                    matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
                                    count_if_matched=False, allow_matching_against_concat_txt=False))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*scope[^a-zA-Z0-9]?1,?[^a-zA-Z0-9]?2.*', score=1,
                                    matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
                                    count_if_matched=False, allow_matching_against_concat_txt=False))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*scope[^a-zA-Z0-9]?1.*relative.*', score=1,
                                    matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
                                    count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct)(?=.*scope[^a-zA-Z0-9]?1).*$(emissions?)?.*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct)(?=.*operated).*$(emissions?)?.*',
            score=6000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*direct).*$(emissions?)?.*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*^(?=.*(gas|ghg|(ghg)|atmospheric))(?=.*scope[^a-zA-Z0-9]?1).*$(emissions?)?.*',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(^|[^a-z])direct.*emissions?.*', score=12000,
                                    matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=30,
                                    letter_decay_disregard=len('direct emissions')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(total|combine).*', score=800, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
                                    letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw='.*direct no.*emissions.*', score=1,
                                                                 matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
                                                                 case_sensitive=False, multi_match_decay=0,
                                                                 letter_decay_hl=10, letter_decay_disregard=0,
                                                                 count_if_matched=False,
                                                                 allow_matching_against_concat_txt=False))
        kpi.unit_regex_match_list.append(
            KPISpecs.GeneralRegExMatch(pattern_raw='.*(ton|mn|million|kt|m t|co 2|co.*emission).*',
                                       case_sensitive=False))

        kpi.value_must_be_numeric = True

        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*(direct|ghg|gas).*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.9,
            multi_match_decay=0.2, letter_decay_hl=8, letter_decay_disregard=len('direct')))
        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*scope[^a-zA-Z0-9]?1.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.7,
            multi_match_decay=0.2, letter_decay_hl=8, letter_decay_disregard=len('direct')))

        # added in particular for CDP reports:
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*gross global scope 1 emissions.*metric.*ton.*', score=20000,
                                    matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False,
                                    multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('gross global scope 1 emissions metric ton')))
        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*c6\.1.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=5000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.9,
            multi_match_decay=0.2, letter_decay_hl=8, letter_decay_disregard=len('c6.1')))
        kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(pattern_raw='.*[0-9].*[0-9].*',
                                                                     case_sensitive=False))  # must contain at least two digits

        kpi.minimum_score = 500
        kpi.minimum_score_desc_regex = 250

        return kpi

    def prepare_kpi_7_scope2_ghg_emissions():
        # KPI 7 = Scope 2 Energy indirect total GHGs emissions
        kpi = KPISpecs()
        kpi.kpi_id = 7
        kpi.kpi_name = 'Scope 2 Energy indirect total GHGs emissions'

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw='.*s.*cope( |-)2.*market', score=5000,
                                                                 matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
                                                                 case_sensitive=False, multi_match_decay=0,
                                                                 letter_decay_hl=20,
                                                                 letter_decay_disregard=len('scope-2 market ')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*s.*cope( |-)2.*', score=8000, matching_mode=MATCHING_MAY_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-2 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*indirect.*ghg.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-2 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-2 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-2 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*co 2.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('CO2')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*market.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope 2  ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*electricity.*', score=500, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-2')))
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(pattern_raw='.*indirect.*emissions.*', score=3000,
                                                                 matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
                                                                 case_sensitive=False, multi_match_decay=1,
                                                                 letter_decay_hl=20, letter_decay_disregard=len('total indirect ghg  scope-2 ')))  # by Lei

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
                                    letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*sale.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
                                    case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*s.*cope( |-)3.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
                                    score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(upstream|refin).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
                                    score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))

        # eq does not work
        kpi.unit_regex_match_list.append(
            KPISpecs.GeneralRegExMatch(pattern_raw='^(t|.*(ton|mn|million|kt|m t|co 2).*)$', case_sensitive=False))

        kpi.value_must_be_numeric = True

        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*(environment|emission).*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=100, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.9,
            multi_match_decay=0.5, letter_decay_hl=5, letter_decay_disregard=len('production')))
        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*total.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=100, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.9,
            multi_match_decay=0.5, letter_decay_hl=5, letter_decay_disregard=len('production')))
        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*tons.*co.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=100, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.05,
            multi_match_decay=0.01, letter_decay_hl=5, letter_decay_disregard=len('tons co2')))  # by Lei
        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*million metric.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=200, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.05,
            multi_match_decay=0.01, letter_decay_hl=5, letter_decay_disregard=len('million metric')))  # by Lei

        kpi.minimum_score = 500
        kpi.minimum_score_desc_regex = 250

        return kpi

    def prepare_kpi_8_scope3_ghg_emissions():
        # KPI 8 = Scope 3
        kpi = KPISpecs()
        kpi.kpi_id = 8
        kpi.kpi_name = 'Scope 3 Upstream Energy indirect total GHGs emissions'

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*s.*cope( |-)3.*', score=8000, matching_mode=MATCHING_MUST_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-3 ')))  # by Lei
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-3 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-3 ')))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*emissions.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=1, case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE,
                                    score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
                                    letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*intensity.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
                                    score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*s.*cope( |-)2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
                                    score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))  # by Lei
        kpi.desc_regex_match_list.append(
            KPISpecs.DescRegExMatch(pattern_raw='.*305.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
                                    case_sensitive=False, multi_match_decay=0, letter_decay_hl=10,
                                    letter_decay_disregard=0, count_if_matched=False,
                                    allow_matching_against_concat_txt=False))  # by Lei

        kpi.unit_regex_match_list.append(
            KPISpecs.GeneralRegExMatch(pattern_raw='.*(ton|mn|million|kt|m t|co 2).*', case_sensitive=False))

        kpi.value_must_be_numeric = True

        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*(environment|emission).*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=100, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.9,
            multi_match_decay=0.5, letter_decay_hl=5, letter_decay_disregard=len('environment')))

        kpi.minimum_score = 500
        kpi.minimum_score_desc_regex = 250

        return kpi

    res = [prepare_kpi_6_scope1_direct_total_ghg_emissions(), prepare_kpi_7_scope2_ghg_emissions(),
           prepare_kpi_8_scope3_ghg_emissions()]
    return res


def load_test_data(test_data_file_path):
    test_data = TestData()
    test_data.load_from_csv(test_data_file_path)

    # for testing purpose:
    test_data.filter_kpis(by_kpi_id=[7], by_data_type=['TABLE'])

    fix_list = DataImportExport.import_files(
        r"//Wwg00m.rootdom.net/afs-team/1200000089/FC/R-M/AZUREPOC/2020/KPIs extraction/Training data/03_Oil Gas sector reports/Europe",
        config.global_input_folder, test_data.get_pdf_list(), 'pdf')
    test_data.fix_file_names(fix_list)

    # filter out entries with no source file:
    test_data.filter_kpis(by_has_fixed_source_file=True)
    return test_data


def test_analyze_directory(htmldirectoy):
    ana = AnalyzerDirectory(htmldirectoy, 2019)
    kpis = test_prepare_kpispecs()

    kpiresults = KPIResultSet(ana.find_multiple_kpis(kpis))

    print_big("FINAL RESULT", do_wait=False)
    print(kpiresults)


def test_result():
    kpiresults = KPIResultSet()
    print(kpiresults)


def demo():
    pdf_file = config.global_input_folder + r'test_bp.pdf'

    print_big("Convert PDF to HTML")
    HTMLDirectory.convert_pdf_to_html(pdf_file)

    print_big("Convert HTML to JSON and PNG")

    dir = HTMLDirectory()
    dir.parse_html_directory(get_html_out_dir(pdf_file), r'page*.html')
    dir.save_to_dir(get_html_out_dir(pdf_file))
    dir.render_to_png(get_html_out_dir(pdf_file), get_html_out_dir(pdf_file))

    print_big("Load from JSON")
    dir = None
    dir = HTMLDirectory()
    dir.load_from_dir(get_html_out_dir(pdf_file), r'jpage*.json')

    print_big("Analyze Tables")
    test_analyze_directory(dir)


def test_main():
    PDF_FILE = config.global_input_folder + r'04_NOVATEK_AR_2016_ENG_11.pdf'
    dir = test_load_json(PDF_FILE, "*")
    test_analyze_directory(dir)


def test_evaluation():
    test_data = load_test_data(r'test_data/aggregated_complete_samples_new.csv')

    test_data.filter_kpis(by_source_file=[
        'Aker-BP-Sustainability-Report-2019.pdf'  # KPIs are on pg: 84: 2009:665.1 ... 2013:575.7
        # , 'NYSE_TOT_2018 annual.pdf'                       # KPIs are on pg: 129: 2017:914, 2018:917
        # , 'Transocean_Sustain_digital_FN_4 2017_2018.pdf'                        # KPIs are on pg: 112: 2016:711.1,  2015: 498.2
        # , 'Wintershall-Dea_Sustainability_Report_2019.pdf'
    ])

    print_big("Data-set", False)
    print(test_data)
    kpiresults = KPIResultSet.load_from_file(r'test_data/kpiresults_test_all_files_against_kpi_2_0.json')
    print_big("Kpi-Results", do_wait=False)
    print(kpiresults)
    print_big("Kpi-Evaluation", do_wait=False)
    kpis = test_prepare_kpispecs()
    test_eval = TestEvaluation.generate_evaluation(kpis, kpiresults, test_data)
    print(test_eval)
