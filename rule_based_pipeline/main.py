# ============================================================================================================================
# PDF_Analyzer
# File   : main.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================
from AnalyzerDirectory import AnalyzerDirectory
import argparse
import config_for_rb
from DataImportExport import DataImportExport
from Format_Analyzer import Format_Analyzer
from globals import file_exists, get_html_out_dir, get_num_of_files, print_verbose, print_big, remove_trailing_slash
from HTMLDirectory import HTMLDirectory
from KPIResultSet import KPIResultSet
import os
from rule_based_pipeline.test import test_prepare_kpi_specs
from TestData import TestData
import time

# Constants Variables
DEFAULT_YEAR = 2022


def parse_arguments():
    """
    Parse command-line arguments and set global configuration variables.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Rule-based KPI extraction')
    parser.add_argument('--raw_pdf_folder', type=str, default=config_for_rb.global_raw_pdf_folder,
                        help='Folder where PDFs are stored')
    parser.add_argument('--working_folder', type=str, default=config_for_rb.global_working_folder,
                        help='Folder where working files are stored')
    parser.add_argument('--output_folder', type=str, default=config_for_rb.global_output_folder,
                        help='Folder where output is stored')
    parser.add_argument('--verbosity', type=int, default=config_for_rb.global_verbosity,
                        help='Verbosity level (0=shut up)')
    # new optional arguments (for Debugging mode): Optional
    parser.add_argument('--name_of_pdf', type=str, default=config_for_rb.global_name_of_pdf,
                        help='Filter Specific PDF')
    parser.add_argument('--page_of_pdf', type=str, default=config_for_rb.global_page_of_table_in_pdf,
                        help='Specific page of the table in the PDF')

    # TODO: why we need this? --> @Marc
    args = parser.parse_args()
    config_for_rb.global_raw_pdf_folder = (remove_trailing_slash(args.raw_pdf_folder).replace("\\", "/") + r"/")
    config_for_rb.global_working_folder = (remove_trailing_slash(args.working_folder).replace("\\", "/") + r"/")
    config_for_rb.global_verbosity = args.verbosity
    config_for_rb.global_output_folder = (remove_trailing_slash(args.output_folder).replace("\\", "/") + r"/")


def fix_config_paths():
    """
    Fix global paths in the configuration.
    This function sets the global paths based on the current directory.

    Returns:
        None
    """
    try:
        path = globals()['_dh'][0]
    except KeyError:
        path = os.path.dirname(os.path.realpath(__file__))
    path = remove_trailing_slash(path).replace('\\', '/')
    config_for_rb.global_exec_folder = path + r'/'
    config_for_rb.global_rendering_font_override = path + r'/' + config_for_rb.global_rendering_font_override
    config_for_rb.global_approx_font_name = path + r'/' + config_for_rb.global_approx_font_name


def make_directories():
    """
    Creates 2 necessary directories (working_folder and output_folder) if they not exist.

    Returns:
        None
    """
    os.makedirs(config_for_rb.global_working_folder, exist_ok=True)
    os.makedirs(config_for_rb.global_output_folder, exist_ok=True)


def print_configuration():
    """
    Print configuration information.

    Returns:
        None
    """
    print_verbose(1, "Using config_for_rb.global_exec_folder=" + config_for_rb.global_exec_folder)
    print_verbose(1, "Using config_for_rb.global_raw_pdf_folder=" + config_for_rb.global_raw_pdf_folder)
    print_verbose(1, "Using config_for_rb.global_working_folder=" + config_for_rb.global_working_folder)
    print_verbose(1, "Using config_for_rb.global_output_folder=" + config_for_rb.global_output_folder)
    print_verbose(1, "Using config_for_rb.global_verbosity=" + str(config_for_rb.global_verbosity))
    print_verbose(1,
                  "Using config_for_rb.global_rendering_font_override=" + config_for_rb.global_rendering_font_override)
    # new optional arguments (for Debugging mode):
    print_verbose(1, "Using config_for_rb.global_name_of_pdf=" + config_for_rb.global_name_of_pdf)
    print_verbose(1, "Using config_for_rb.global_page_of_table_in_pdf=" + config_for_rb.global_page_of_table_in_pdf)


def analyze_and_save_results(pdf_name, kpis, info_file_contents):
    """
    Analyze the specified PDF, save the results, and print verbose information.

    Args:
        pdf_name (str): The name of the PDF file.
        kpis (list): List of KPI specifications.
        info_file_contents (dict): Information loaded from an info file.

    Returns:
        KPIResultSet: Results of the analysis.
    """
    kpi_results = KPIResultSet()
    # to analyze specific page, add e.g.:  wildcard_restrict_page=*00042
    input_pdf = config_for_rb.global_raw_pdf_folder + pdf_name
    cur_kpi_results = analyze_pdf(input_pdf, kpis, info_file_contents)
    kpi_results.extend(cur_kpi_results)
    kpi_results.save_to_csv_file(config_for_rb.global_output_folder + pdf_name + r'.csv')
    print_verbose(1, "RESULT FOR " + pdf_name)
    print_verbose(1, kpi_results)
    return kpi_results


def generate_dummy_test_data():
    """
    This function creates a TestData object and generates dummy test data from raw_pdf folder (all PDFs in raw_pdf folder).

    Returns:
        TestData: An instance of TestData with dummy test data from raw_pdf (all PDFs in raw_pdf folder).
    """
    # Create a TestData object
    test_data = TestData()

    # Generate dummy test data from raw_pdf
    test_data.generate_dummy_test_data(config_for_rb.global_raw_pdf_folder)

    # Return the populated TestData object
    return test_data


def analyze_pdf(pdf_file, kpis, info_file_contents, wildcard_restrict_page='*', force_pdf_convert=False,
                force_parse_pdf=False, assume_conversion_done=False, do_wait=False):
    """
    Analyze the specified PDF, save the results, and print verbose information.

    Args:
        pdf_file (str): The name of the PDF file.
        kpis (list): List of KPI specifications.
        info_file_contents (dict): Information loaded from an info file.
        wildcard_restrict_page (str): Page wildcard.
        force_pdf_convert (bool): If True, forces PDF to HTML conversion.
        force_parse_pdf (bool): If True, forces HTML to JSON and PNG conversion.
        assume_conversion_done (bool): If True, assumes conversion is done.
        do_wait (bool): If True, display a progress indicator.

    Returns:
        KPIResultSet: Results of the analysis.
    """
    print_verbose(1, "Analyzing PDF: " + str(pdf_file))

    guess_year = Format_Analyzer.extract_year_from_text(pdf_file)
    guess_year = guess_year if guess_year is not None else DEFAULT_YEAR

    html_dir_path = get_html_out_dir(pdf_file)
    os.makedirs(html_dir_path, exist_ok=True)

    convert_pdf_to_html(pdf_file, html_dir_path, force_pdf_convert, info_file_contents, do_wait)

    if not assume_conversion_done:
        # parse and create json and png
        convert_html_to_json_and_png(html_dir_path, force_parse_pdf, do_wait)

    directory = load_json_files(html_dir_path, do_wait, wildcard_restrict_page)

    kpi_results = analyze_pages(directory, guess_year, kpis, do_wait)

    print_big("FINAL RESULT FOR: " + str(pdf_file.upper()), do_wait)
    print_verbose(1, kpi_results)

    return kpi_results


def convert_pdf_to_html(pdf_file, html_dir_path, force_pdf_convert=False, info_file_contents=None, do_wait=False):
    """
    Convert PDF to HTML.

    Args:
        pdf_file (str): Path to the PDF file.
        html_dir_path (str): Directory to store HTML files.
        force_pdf_convert (bool): If True, forces PDF to HTML conversion.
        info_file_contents (dict): Information loaded from an info file.
        do_wait (bool): If True, display a progress indicator.

    Returns:
        None
    """
    print_big("Convert PDF to HTML", do_wait)
    if force_pdf_convert or not file_exists(os.path.join(html_dir_path, 'index.html')):
        HTMLDirectory.convert_pdf_to_html(pdf_file, info_file_contents)


def convert_html_to_json_and_png(html_dir_path, force_parse_pdf=False, do_wait=False):
    """
    Convert HTML to JSON and PNG.

    Args:
        html_dir_path (str): Directory containing HTML files.
        force_parse_pdf (bool): If True, forces HTML to JSON and PNG conversion.
        do_wait (bool): If True, display a progress indicator.

    Returns:
        None
    """
    print_big("Convert HTML to JSON and PNG", do_wait)
    html_directory = HTMLDirectory()
    if (force_parse_pdf or get_num_of_files(os.path.join(html_dir_path, 'jpage*.json')) != get_num_of_files(
            os.path.join(html_dir_path, 'page*.html'))):
        html_directory.parse_html_directory(html_dir_path, 'page*.html')  # ! page*
        html_directory.render_to_png(html_dir_path, html_dir_path)
        html_directory.save_to_dir(html_dir_path)


def load_json_files(html_dir_path, do_wait, wildcard_restrict_page='*'):
    """
    Load JSON files.

    Args:
        html_dir_path (str): Directory containing JSON files.
        do_wait (bool): If True, display a progress indicator.
        wildcard_restrict_page (str): Page wildcard.

    Returns:
        HTMLDirectory: Loaded HTML directory.
    """
    print_big("Load from JSON", do_wait)
    directory = HTMLDirectory()
    directory.load_from_dir(html_dir_path, 'jpage' + str(wildcard_restrict_page) + '.json')
    return directory


def analyze_pages(directory, guess_year, kpis, do_wait):
    """
    Analyze HTML pages.

    Args:
        directory (HTMLDirectory): HTML directory.
        guess_year (int): Guessed year.
        kpis (list): List of KPI specifications.
        do_wait (bool): If True, display a progress indicator.

    Returns:
        KPIResultSet: Results of the analysis.
    """
    print_big("Analyze Pages", do_wait)
    ana = AnalyzerDirectory(directory, guess_year)
    kpi_results = KPIResultSet(ana.find_multiple_kpis(kpis))
    return kpi_results


def main():
    parse_arguments()

    # Fix global paths
    fix_config_paths()

    # make directories if not exist
    make_directories()

    # Print configuration information
    print_configuration()

    # Generate dummy test data
    test_data = generate_dummy_test_data()

    # Filter PDF
    # test_data.filter_kpis(by_source_file=['T_Rowe_Price_2021_EN.pdf'])

    # Print information about the test data
    print_big("Data-set", False)
    print_verbose(1, test_data)

    # Get a list of PDFs from the test data
    pdfs = test_data.get_unique_list_of_pdf_files()
    print_verbose(1, 'Related (fixed) PDFs: ' + str(pdfs) + ', in total : ' + str(len(pdfs)))

    # Prepare KPI specifications
    kpis = test_prepare_kpi_specs()

    # Initialize overall KPI results
    overall_kpi_results = KPIResultSet()

    # Load information from the file info.json
    json_file_name = remove_trailing_slash(config_for_rb.global_working_folder) + '/info.json'
    info_file_contents = DataImportExport.load_path_files_from_json_file(json_file_name)

    # Record the start time for performance measurement
    time_start = time.time()

    # Iterate over each PDF in the list
    for pdf in pdfs:
        # Analyze the current PDF
        kpi_results = analyze_and_save_results(pdf, kpis, info_file_contents)
        overall_kpi_results.extend(kpi_results)

    # Record the finish time for performance measurement
    time_finish = time.time()

    # Print the final overall result
    print_big("FINAL OVERALL-RESULT", do_wait=False)
    print_verbose(1, overall_kpi_results)

    # Save overall KPI results to a CSV file
    overall_kpi_results.save_to_csv_file(config_for_rb.global_output_folder + r'kpi_results_tmp.csv')

    # Calculate and print the total run-time
    total_time = time_finish - time_start
    print_verbose(1, "Total run-time: " + str(total_time) + " sec ( " + str(
        total_time / max(len(pdfs), 1)) + " sec per PDF)")


# Entry point of the program
if __name__ == "__main__":
    main()
