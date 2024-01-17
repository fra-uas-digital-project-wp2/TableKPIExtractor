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
SRC_DIR = os.path.join(path, "20240114_Expected_Values")
OUT_DIR = os.path.join(path, "20240114_Expected_Values_Converted")
RAW_DIR = os.path.join(path, "input2")

print(SRC_DIR)

NAME_DICT = {
             "Scope 1" : "Scope 1 / Direct total GHGs emissions",
             "Scope 2" : "Scope 2 Energy indirect total GHGs emissions",
             "Scope 3" : "Scope 3 Upstream Energy indirect total GHGs emissions",
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
    
def write_csv_header(filename, header):
    full_path = os.path.join(OUT_DIR,filename+".csv")
    with open(full_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)

def write_csv_lines(filename, lines):
    full_path = os.path.join(OUT_DIR,filename+".csv")
    with open(full_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for line in lines:
            csv_writer.writerow(line)

def check_exists(filename):
    full_path = os.path.join(RAW_DIR,filename+".pdf")
    if os.path.exists(full_path):
        return True
    else:
        return False

def extract_data(file,data):
    return_data = []
    for keys in data.keys():
        scope = data.get(keys)

        for idx in range(len(scope.get("Value"))):
            # 0 KPI_ID | 1 KPI_NAME | 2 SRC_FILE | 3 PAGE_NUM | - | - | - | 7 RAW_TXT | 8 YEAR | 9 VALUE | - | 11 UNIT | - 
            row = ['-'] * 13
            row[0] = scope.get("ID")
            row[1] = NAME_DICT.get(keys)
            row[2] = file
            row[3] = scope.get("Page")[idx]
            row[7] = scope.get("Value")[idx]
            row[8] = scope.get("Year")[idx]
            row[9] = scope.get("Value")[idx]

        return_data.append(row)
    return return_data




def main():

    logger = create_logger()
    no_files = 0
    problematics = []
    empty_pdfs = []
    header = [
        "KPI_ID", "KPI_NAME", "SRC_FILE", "PAGE_NUM", "ITEM_IDS", "POS_X",
        "POS_Y", "RAW_TXT", "YEAR", "VALUE", "SCORE", "UNIT", "MATCH_TYPE"
    ]
    missing_names = []
    
    for file in os.listdir(SRC_DIR):
        
        try:
            data = load(file)
            file = file[:-5]
            no_files += 1

            write_csv_header(file,header)

            if is_empty(data,"Scope 1") and is_empty(data,"Scope 2") and is_empty(data,"Scope 3"):
                empty_pdfs.append(file)
                continue
            
            formatted_data = extract_data(file,data)
            
            if not check_exists(file):
                missing_names.append(file)

            write_csv_lines(file,formatted_data)

        except Exception as e:
            problematics.append(file)
            logger.error(f"File '{file}' had exception '{e}' ")

    print(f"Number of files '{no_files}'")
    print(f"Number of empty files '{len(empty_pdfs)}'")
    print(f"Number of problematic pdfs '{len(problematics)}'")
    print(f"Number of pdfs without raw '{len(missing_names)}'")
    print(f"Problematics \n '{problematics}'")
    print(f"Missings \n '{missing_names}'")

if __name__ == "__main__":
    main()