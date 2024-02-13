# ============================================================================================================================
# EnergyEmissionsKPIAnalyzer
# File   : EnergyEmissionsKPIAnalyzer.py
# Author : Zakaria Jouahri
# Date   : 31.12.2023
# ============================================================================================================================
from KPISpecs import KPISpecs

# Matching modes:
MATCHING_MUST_INCLUDE = 0  # no match, if not included
MATCHING_MAY_INCLUDE = 1  # should be included, but inclusion is not necessary, although AT LEAST ONE such item must be included. can also have a negative score
MATCHING_CAN_INCLUDE = 2  # should be included, but inclusion is not necessary. can also have a negative score
MATCHING_MUST_EXCLUDE = 3  # no match, if included

# Distance modes
DISTANCE_MOD_EUCLID = 1  # euclidian distance, but with modification such that orthogonal aligned objects are given a smaller distance (thus preferring table-like alignments)


def prepare_kpi_specs():
    """
        Prepares a list of KPIs related to energy emissions.

        Returns:
            list: A list of KPISpecs objects.
    """
    def prepare_kpi_6_scope1():
        # KPI 6 = Scope 1 / Direct total GHGs emissions
        kpi = KPISpecs()
        kpi.kpi_id = 6
        kpi.kpi_name = 'Scope 1 / Direct total GHGs emissions'

        # Match paragraphs
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2).*emissions?.*', score=7000,
            matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gas emissions')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])co2.*emissions?.*tCO2e.*', score=10000, matching_mode=MATCHING_MAY_INCLUDE,
            score_decay=0.1, case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('co2 emissions')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*scope[^a-zA-Z0-9]?1.*', score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20, letter_decay_disregard=len('scope 1')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric|co2|combustion.*fuels?).*emissions?.*',
            score=7000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gas emissions')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])combustion.*fuels?.*', score=6000,
            matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gas emissions')))

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

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*scope\s1.*', score=6000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=30,
            letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])(greenhouse)?.*(gas|ghg|(ghg)|atmospheric).*direct.*scope[^a-zA-Z0-9]?1(emissions?)?.*m.*t',
            score=12000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=30, letter_decay_disregard=len('proven reserves of oil and gas')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*scope[^a-zA-Z0-9]?2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

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

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(scope[^a-zA-Z0-9]?2|scope[^a-zA-Z0-9]?3).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
            score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*scope[^a-zA-Z0-9]?1,?[^a-zA-Z0-9]?2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
            score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*scope[^a-zA-Z0-9]?1.*relative.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE,
            score_decay=0, case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
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

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(^|[^a-z])direct.*emissions?.*', score=12000, matching_mode=MATCHING_MAY_INCLUDE,
            score_decay=0.8, case_sensitive=False, multi_match_decay=0, letter_decay_hl=30,
            letter_decay_disregard=len('direct emissions')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(total|combine).*', score=800, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*direct no.*emissions.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='.*(ton|mn|million|kt|m t|co 2|co.*emission).*', case_sensitive=False))

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
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*gross global scope 1 emissions.*metric.*ton.*', score=20000,
            matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.1, case_sensitive=False, multi_match_decay=0,
            letter_decay_hl=20, letter_decay_disregard=len('gross global scope 1 emissions metric ton')))

        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*c6\.1.*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=5000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.9,
            multi_match_decay=0.2, letter_decay_hl=8, letter_decay_disregard=len('c6.1')))

        kpi.value_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='.*[0-9].*[0-9].*', case_sensitive=False))  # must contain at least two digits

        kpi.minimum_score = 500
        kpi.minimum_score_desc_regex = 250

        return kpi

    def prepare_kpi_7_scope2():
        # KPI 7 = Scope 2 Energy indirect total GHGs emissions
        kpi = KPISpecs()
        kpi.kpi_id = 7
        kpi.kpi_name = 'Scope 2 Energy indirect total GHGs emissions'


        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*', score=16000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*ghg.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*co 2.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20, letter_decay_disregard=len('CO2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*electricity.*', score=500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*emissions.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))  # by Lei

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*sale.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
            multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0, count_if_matched=False,
            allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)3.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)1.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*location.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*market.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(upstream|refin).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        # eq does not work
        kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='^(t|.*(ton|mn|million|kt|m t|co 2).*)$', case_sensitive=False))

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

    def prepare_kpi_8_scope3():
        # KPI 8 = Scope 3
        kpi = KPISpecs()
        kpi.kpi_id = 8
        kpi.kpi_name = 'Scope 3 Upstream Energy indirect total GHGs emissions'

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)3.*', score=8000, matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*emissions.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=1,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-3 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*intensity.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*305.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
            multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0, count_if_matched=False,
            allow_matching_against_concat_txt=False))

        kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='.*(ton|mn|million|kt|m t|co 2).*', case_sensitive=False))

        kpi.value_must_be_numeric = True

        kpi.anywhere_regex_match_list.append(KPISpecs.AnywhereRegExMatch(
            general_match=KPISpecs.GeneralRegExMatch(pattern_raw='.*(environment|emission).*', case_sensitive=False),
            distance_mode=DISTANCE_MOD_EUCLID, score=100, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.9,
            multi_match_decay=0.5, letter_decay_hl=5, letter_decay_disregard=len('environment')))

        kpi.minimum_score = 500
        kpi.minimum_score_desc_regex = 250

        return kpi
    
    def prepare_kpi_9_scope2_market():
        kpi = KPISpecs()
        kpi.kpi_id = 9
        kpi.kpi_name = 'Scope 2 Market Energy indirect total GHGs emissions'

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*market', score=5000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('scope-2 market ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*', score=8000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*ghg.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*co 2.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20, letter_decay_disregard=len('CO2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*market.*', score=3000, matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope 2  ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*electricity.*', score=500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*emissions.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))  # by Lei

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*sale.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
            multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0, count_if_matched=False,
            allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)3.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)1.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*location.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(upstream|refin).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        # eq does not work
        kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='^(t|.*(ton|mn|million|kt|m t|co 2).*)$', case_sensitive=False))

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
    
    def prepare_kpi_10_scope2_location():
        
        kpi = KPISpecs()
        kpi.kpi_id = 10
        kpi.kpi_name = 'Scope 2 Location Energy indirect total GHGs emissions'

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*location', score=5000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('scope-2 location ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)2.*', score=8000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*ghg.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*ghg.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*', score=3000, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*co 2.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=20, letter_decay_disregard=len('CO2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*location.*', score=3000, matching_mode=MATCHING_MUST_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope 2  ')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*electricity.*', score=500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*indirect.*emissions.*', score=3000, matching_mode=MATCHING_MAY_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=20,
            letter_decay_disregard=len('total indirect ghg  scope-2 ')))  # by Lei

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(total|combine).*', score=1500, matching_mode=MATCHING_CAN_INCLUDE, score_decay=0.8,
            case_sensitive=False, multi_match_decay=1, letter_decay_hl=10,
            letter_decay_disregard=len('total indirect ghg  scope-2')))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*sale.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0, case_sensitive=False,
            multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0, count_if_matched=False,
            allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)3.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*s.*cope( |-)1.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))
        
        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*market.*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        kpi.desc_regex_match_list.append(KPISpecs.DescRegExMatch(
            pattern_raw='.*(upstream|refin).*', score=1, matching_mode=MATCHING_MUST_EXCLUDE, score_decay=0,
            case_sensitive=False, multi_match_decay=0, letter_decay_hl=10, letter_decay_disregard=0,
            count_if_matched=False, allow_matching_against_concat_txt=False))

        # eq does not work
        kpi.unit_regex_match_list.append(KPISpecs.GeneralRegExMatch(
            pattern_raw='^(t|.*(ton|mn|million|kt|m t|co 2).*)$', case_sensitive=False))

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

    result = [prepare_kpi_6_scope1(), prepare_kpi_7_scope2(), prepare_kpi_8_scope3(),prepare_kpi_9_scope2_market(),prepare_kpi_10_scope2_location()]
    return result
