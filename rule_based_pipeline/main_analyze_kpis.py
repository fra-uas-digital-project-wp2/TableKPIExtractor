import os
import logging
import json
import csv 

from logging.handlers import RotatingFileHandler

try:
        path = globals()['_dh'][0]
except KeyError:
        path = os.path.dirname(os.path.realpath(__file__))
print(path)
#SRC_DIR = os.path.join(path, "20240114_Expected_Values")
SRC_DIR = os.path.join(path, "Expected_Values_Appended")
#OUT_DIR = os.path.join(path, "20240114_Expected_Values_Converted")
RAW_DIR = os.path.join(path, "input2")

print(SRC_DIR)

NAME_DICT = {
             "Scope 1" : "Scope 1 / Direct total GHGs emissions",
             "Scope 2" : "Scope 2 Energy indirect total GHGs emissions",
             "Scope 3" : "Scope 3 Upstream Energy indirect total GHGs emissions",
             "Scope 2 Market" : 'Scope 2 Market Energy indirect total GHGs emissions',
             "Scope 2 Location" : 'Scope 2 Location Energy indirect total GHGs emissions', 
            }

def create_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)


    # Create a RotatingFileHandler with a max file size of 1MB and a maximum of 5 backup files
    file_handler = RotatingFileHandler('conversion.log', maxBytes=1024*1024, backupCount=5,encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger

def load(file):
    full_path = os.path.join(SRC_DIR,file)
    print(full_path)
    f = open(full_path)
    return json.load(f)

def is_empty(data,key):

    l = data.get(key).get("Value") 
    if len(l) == 0: 
        return True
    else:
        return False
    

def check_exists(filename):
    full_path = os.path.join(RAW_DIR,filename+".pdf")
    if os.path.exists(full_path):
        return True
    else:
        return False

def count(data,key,cnt):
    return len(data.get(key).get("Value")) 


def main():

    logger = create_logger()
    no_files = 0
    no_true_data = 0
    problematics = []
    empty_pdfs = []
    non_empty = []
    ToDo = []
    missing_names = []
    
    for file in os.listdir(SRC_DIR):
        
        try:
            data = load(file)
            file = file[:-5]
            no_files += 1

            if not check_exists(file):
                missing_names.append(file)


            if is_empty(data,"Scope 1") and is_empty(data,"Scope 2") and is_empty(data,"Scope 3") and is_empty(data,"Scope 2 Location") and is_empty(data,"Scope 2 Market"):
                empty_pdfs.append(file)
                continue
            non_empty.append(file)
            no_true_data += count(data,"Scope 1",no_true_data)
            no_true_data += count(data,"Scope 2",no_true_data)
            no_true_data += count(data,"Scope 3",no_true_data)
            no_true_data += count(data,"Scope 2 Location",no_true_data)
            no_true_data += count(data,"Scope 2 Market",no_true_data)
            
            count

        except Exception as e:
            problematics.append(file)
            logger.error(f"File '{file}' had exception '{e}' ")

    print(f"Number of files '{no_files}'")
    print(f"Number of empty files '{len(empty_pdfs)}'")
    print(f"Number of problematic pdfs '{len(problematics)}'")
    print(f"Number of pdfs without raw '{len(missing_names)}'")
    print(f"True Data Values '{no_true_data}'")
    print(f"Problematics \n '{problematics}'")
    print(f"Missings \n '{missing_names}'")
    print(f"Non-Empty PDFs \n '{non_empty}'")
if __name__ == "__main__":
    main()