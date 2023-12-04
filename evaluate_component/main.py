import logging 
import os
import json
import pandas as pd
import argparse
import config
from Evaluate import *



log_file_name = 'app.log'

try:
    log_dir_name = globals()['_dh'][0]
except KeyError:
    log_dir_name = os.path.dirname(os.path.realpath(__file__))
log = os.path.join(log_dir_name,log_file_name)
logging.basicConfig(level=logging.DEBUG,filename=log, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


parser = argparse.ArgumentParser(description='Rule-based KPI extraction')
parser.add_argument('--input_folder', type=str, default=config.global_input_folder,
                    help='Folder where PDFs are stored')
parser.add_argument('--expected_folder', type=str, default=config.global_expected_folder,
                    help='Folder where expected files are stored')
parser.add_argument('--output_folder', type=str, default=config.global_output_folder_evaluate,
                    help='Folder where output is stored')
args = parser.parse_args()

EXPECTED_PATH = args.input_folder
TRUE_PATH = args.expected_folder
RESULT_PATH = args.output_folder

eval = Evaluate(RESULT_PATH)

# Iteratve over Output from OS-C
for filename in os.listdir(EXPECTED_PATH):
    expec_path = os.path.join(EXPECTED_PATH,filename)

    

    # Substring on filename
    fName_no_ending = filename.split(".")[0]
    true_path = os.path.join(TRUE_PATH,fName_no_ending+".json")
    # Check if corresponding file exists, if not log error and continue
    if not(os.path.isfile(true_path)):
        logging.error("For output: " + filename + " no corresponding true output does exist!")
        continue

    true_dict = json.load(open(true_path,'r'))
    expec_csv = pd.read_csv(expec_path) 

    logging.debug(f"Current File '{fName_no_ending}'")
    eval.evaluate(true_dict,expec_csv,fName_no_ending)

eval.output_result()
    
        



 