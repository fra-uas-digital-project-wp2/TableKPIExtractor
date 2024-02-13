# ============================================================================================================================
# PDF_Analyzer
# File   : main.py
# Author : Ismail Demir (G124272)
# Date   : 12.06.2020
# ============================================================================================================================
import argparse
import config_for_rb
import jsonpickle
import os
import shutil
import time
import sys
import multiprocessing as mp
import logging

from AnalyzerDirectory import AnalyzerDirectory
from FormatAnalyzer import FormatAnalyzer
from globals import file_exists, get_html_out_dir, get_num_of_files, print_verbose, print_big, remove_trailing_slash
from HTMLDirectory import HTMLDirectory
from KPIResultSet import KPIResultSet
from PreparationOfKPISpecs import prepare_kpi_specs
from TestData import TestData
from logging.handlers import RotatingFileHandler
from TestEvaluation import TestEvaluation

# Constants Variables
DEFAULT_YEAR = 2022


def create_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)


    # Create a RotatingFileHandler with a max file size of 1MB and a maximum of 5 backup files
    file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5,encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    #open('app.log', 'w').close()

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger


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
    config_for_rb.global_raw_pdf_folder = path + r'/' + config_for_rb.global_raw_pdf_folder
    config_for_rb.global_output_folder = path + r'/' + config_for_rb.global_output_folder
    config_for_rb.global_working_folder = path + r'/' + config_for_rb.global_working_folder
    config_for_rb.global_rendering_font_override = path + r'/' + config_for_rb.global_rendering_font_override
    config_for_rb.global_approx_font_name = path + r'/' + config_for_rb.global_approx_font_name
    config_for_rb.global_expected_values_folder = path + r'/' + config_for_rb.global_expected_values_folder 
    config_for_rb.global_evaluation_results_folder = path + r'/' + config_for_rb.global_evaluation_results_folder


def make_directories():
    """
    Creates 3 necessary directories if they not exist.

    Returns:
        None
    """
    if config_for_rb.global_reset_workdir and os.path.exists(config_for_rb.global_working_folder) and os.path.isdir(config_for_rb.global_working_folder):
        shutil.rmtree(config_for_rb.global_working_folder)

    os.makedirs(config_for_rb.global_working_folder, exist_ok=True)
    os.makedirs(config_for_rb.global_output_folder, exist_ok=True)
    os.makedirs(config_for_rb.global_evaluation_results_folder, exist_ok=True)


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


def analyze_all_pdfs(pdfs, kpis, info_file_contents,overall_kpi_results):
    if config_for_rb.global_debug_mode:
        single_process_analysis(pdfs, kpis, info_file_contents,overall_kpi_results)
    else:
        multi_process_analysis(pdfs, kpis, info_file_contents,overall_kpi_results)

def single_process_analysis(pdfs, kpis, info_file_contents,overall_kpi_results): 
    for pdf in pdfs:
        # Analyze the current PDF
        kpi_results = analyze_and_save_results(pdf, kpis, info_file_contents)
        overall_kpi_results.extend(kpi_results)

def multi_process_analysis(pdfs, kpis, info_file_contents,overall_kpi_results):
    cores = mp.cpu_count()
    queue = mp.Queue()
    for pdf in pdfs:
        queue.put(pdf)
    
    paths = []
    paths.append(config_for_rb.global_exec_folder)
    paths.append(config_for_rb.global_raw_pdf_folder)
    paths.append(config_for_rb.global_output_folder)
    paths.append(config_for_rb.global_working_folder)
    paths.append(config_for_rb.global_rendering_font_override)
    paths.append(config_for_rb.global_approx_font_name)

    processes = []
    for _ in range(cores):
        p = mp.Process(target=mp_task,args = (queue,kpis, info_file_contents,overall_kpi_results,paths))
        processes.append(p)
        p.deamon = True
        p.start()

    print(processes)

    for p in processes:
        print(f"Parent process ID: {os.getpid()}")
        print(f"Child process ID: {p.pid}")
        p.join()
    print("All processes have finished.")

def mp_task(queue,kpis, info_file_contents,overall_kpi_results,paths):
    # Additional exception handling if needed

    config_for_rb.global_exec_folder = paths[0]
    config_for_rb.global_raw_pdf_folder = paths[1]
    config_for_rb.global_output_folder = paths[2] 
    config_for_rb.global_working_folder = paths[3] 
    config_for_rb.global_rendering_font_override = paths[4] 
    config_for_rb.global_approx_font_name = paths[5]

    while not queue.empty(): 
        try:
            pdf = queue.get(block=False)
            print(f"PDF = '{pdf}'")
            kpi_results = analyze_and_save_results(pdf, kpis, info_file_contents)
            overall_kpi_results.extend(kpi_results)
        except Exception as e:
            print(f"The following exception occurred '{e}'!")
            break
    sys.exit()


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

    guess_year = FormatAnalyzer.extract_year_from_text(pdf_file)
    guess_year = guess_year if guess_year is not None else DEFAULT_YEAR

    html_dir_path = get_html_out_dir(pdf_file)
    os.makedirs(html_dir_path, exist_ok=True)

    convert_pdf_to_html(pdf_file, html_dir_path, force_pdf_convert, info_file_contents, do_wait)

    if not assume_conversion_done:
        # parse and create json and png
        directory = convert_html_to_json_and_png(html_dir_path, force_parse_pdf, do_wait)

    if config_for_rb.global_debug_mode:
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
        html_directory : HTMLDirectory Object
    """
    print_big("Convert HTML to JSON and PNG", do_wait)
    html_directory = HTMLDirectory()
    if (force_parse_pdf or get_num_of_files(os.path.join(html_dir_path, 'jpage*.json')) != get_num_of_files(
            os.path.join(html_dir_path, 'page*.html'))):

        html_directory.parse_html_directory(html_dir_path, 'page*.html')

        if config_for_rb.global_debug_mode:
            html_directory.render_to_png(html_dir_path, html_dir_path)
            html_directory.save_to_dir(html_dir_path)

    return html_directory


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


def load_all_path_files_from_info_json_file(json_file):
    """
    Load the paths of the files from a JSON file info.json.

    Args:
        json_file (str): Path to the JSON file.

    Returns:
        json_data (str): The loaded json data.
    """
    with open(json_file, "r") as file:
        data = file.read()
    json_data = jsonpickle.decode(data)
    return json_data

def evaluation(logger):

    actual_values = TestData() # Output 
    expected_values = KPIResultSet() #Expected Values

    for file in os.listdir(config_for_rb.global_output_folder):
        file = file[:-8]
        if file == "kpi_results":
            continue

        actual_values.load_from_csv(os.path.join(config_for_rb.global_output_folder,file+".pdf.csv"))

        expected_values.extend(
            KPIResultSet.load_from_csv(
                os.path.join(config_for_rb.global_expected_values_folder,file+".csv")))

    print_big("Kpi-Evaluation", do_wait=False)
    test_eval = TestEvaluation.generate_evaluation("", expected_values, actual_values)

    logger.info(f"True Positives : '{test_eval.num_true_positive}'")
    logger.info(f"False Positives : '{test_eval.num_false_positive}'")
    logger.info(f"True Negatives : '{test_eval.num_true_negative}'")
    logger.info(f"False Negatives : '{test_eval.num_true_positive}'")
    logger.info(f"Precision : '{round(test_eval.measure_precision,3)}'")
    logger.info(f"Recall : '{round(test_eval.measure_recall,3)}'")
    logger.info(f"Accuracy : '{round(test_eval.measure_accuracy,3)}'")


    print(test_eval)



    pass


def main():



    logger = create_logger()
    # Record the start time for performance measurement
    time_start = time.time()
    logger.info(f"Start Time: '{time_start}'")

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
    kpis = prepare_kpi_specs()

    # Initialize overall KPI results
    overall_kpi_results = KPIResultSet()

    # Load information from the file info.json
    json_file_name = remove_trailing_slash(config_for_rb.global_working_folder) + '/info.json'
    info_file_contents = load_all_path_files_from_info_json_file(json_file_name)

    # Iterate over each PDF in the list
    if not (config_for_rb.global_evaluation_only):
        analyze_all_pdfs(pdfs, kpis, info_file_contents,overall_kpi_results)

    # Record the finish time for performance measurement
    time_finish = time.time()
    logger.info(f"End Time: '{time_finish}'")

    # Record the finish time for performance measurement
    time_finish = time.time()

    # Print the final overall result
    print_big("FINAL OVERALL-RESULT", do_wait=False)
    print_verbose(1, overall_kpi_results)

    # Save overall KPI results to a CSV file
    overall_kpi_results.save_to_csv_file(config_for_rb.global_output_folder + r'kpi_results_tmp.csv')

    evaluation(logger)

    # Calculate and print the total run-time
    total_time = time_finish - time_start
    print_verbose(1, "Total run-time: " + str(total_time) + " sec ( " + str(
        total_time / max(len(pdfs), 1)) + " sec per PDF)")
    logger.info("Total run-time: " + str(total_time) + " sec ( " + str(
        total_time / max(len(pdfs), 1)) + " sec per PDF)")


# Entry point of the program
if __name__ == "__main__":
    main()
