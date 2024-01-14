# ============================================================================================================================
# PDF_Analyzer
# File   : config.py
# Author : Ismail Demir (G124272)
# Date   : 17.02.2022
# ============================================================================================================================


# Change verbosity here. verbosity 6-8 are good values for debugging without too much output
global_verbosity = 1

global_exec_folder = r"./rule_based_pipeline/"

global_raw_pdf_folder = r"raw_pdf/"
global_input_folder = r"input/"
global_working_folder = r"workdir/"
global_output_folder = r"output/"
global_expected_values_folder = r"expected_values/"


# Filter PDFs and pages
global_name_of_pdf = "*"
global_page_of_table_in_pdf = "*"

global_debug_mode = False  # default: False. If true, detected tables are printed and HTMLDirectory is serialized.


global_rendering_font_override = r"default_font.otf"
global_approx_font_name = r"default_font.otf"  # use this font as approximation
global_max_identify_complex_items_timeout = 0.5  # seconds

global_force_special_items_into_table = True
global_row_connection_threshold = 10.0  # default=5 . If there is empty space for that many times the previous row height, we will consider this as two distinct tables
global_be_more_generous_with_good_tables = True  # default=False. If true, we will consider some tables as good that normally considered bad

global_table_merge_non_overlapping_rows = True  # default: Fale. If true, system will try to merge non-overlapping rows that probably belong to the same cell

global_html_encoding = "utf-8"  # default: "ascii"

global_ignore_all_years = False  # default: False. Set it to true to ignore all years for every KPI (this is used for CDP reports)

global_analyze_multiple_pages_at_one = False  # default: False. Set it to True, to additionally search for KPIs on multiple (currently: 2) subsequent pages at once.
