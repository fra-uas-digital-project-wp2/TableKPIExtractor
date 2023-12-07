import os 
import subprocess
import config
import logging



# constants 
ABS_DIR = os.path.dirname(os.path.realpath(__file__))
REL_RULE_BASED_DIR = config.global_rule_based_folder
REL_OUT_COMP_DIR = config.global_out_comp_folder

log_file_name = 'app.log'

    
log = os.path.join(ABS_DIR,log_file_name)
logging.basicConfig(level=logging.DEBUG,filename=log, filemode='w', format='%(name)s - %(levelname)s - %(message)s')



def exec_rule_based_engine():
    rule_based_dir = os.path.join(ABS_DIR,REL_RULE_BASED_DIR)
    
    rule_based_arguments = [
                            '--raw_pdf_folder',config.global_input_folder,
                            '--output_folder',config.global_output_folder_rulebased,
                            '--verbosity',config.verbosity,
                            '--working_folder',config.global_working_folder
                            #'--working_folder',working_folder,
                            ] 

    exec = os.path.join(rule_based_dir,'main.py')
    result = subprocess.run(['python', exec] + rule_based_arguments,check=True)

    # Check the exit code
    if result.returncode == 0:
        logging.info(f"Script {exec} has finished successfully.")
        return True
    else:
        logging.error(f"Script {exec} exited with an error. Exit code: {result.returncode}")
        return False

def exec_evaluate_component():
    out_comp_dir = os.path.join(ABS_DIR,REL_OUT_COMP_DIR)
    out_comp_arguments = ['--input_folder',config.global_output_folder_rulebased,
                          '--expected_folder',config.global_expected_folder,
                          '--output_folder',config.global_output_folder_evaluate

    ]

    exec = os.path.join(out_comp_dir,'main.py')
    result = subprocess.run(['python',exec] + out_comp_arguments, check=True)

    if result.returncode == 0:
        logging.info(f"Script {exec} has finished successfully.")
        return True
    else:
        logging.error(f"Script {exec} exited with an error. Exit code: {result.returncode}")
        return False

def main():
    
    success = exec_rule_based_engine()
    
    if not success:
        return 0    
    
    success = exec_evaluate_component()
    
    if success:
        return 1
    else:
        return 0

main()