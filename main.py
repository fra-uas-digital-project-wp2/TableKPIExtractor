import logging 
import os
import json
import pandas as pd
from Evaluate import *


logging.basicConfig(level=logging.DEBUG,filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


EXPECTED_PATH = r"Output_Of_OS_Climate/" 
TRUE_PATH = r"Expected_Values/"
RESULT_PATH = r"Quality_Matrix/"


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
    eval.evaluate(true_dict,expec_csv)

eval.output_result()
    
        



 