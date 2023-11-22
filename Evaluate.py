import json
import logging
import csv
import os
class Evaluate:
    
    cnt = 0

    true_dict = None
    expec_pd = None

    total_accuracy = 0
    
    scope_accuracy = {
        "Scope 1" : 0,
        "Scope 2" : 0,
        "Scope 3" : 0,
    }
    
    # Variables for a single file
    
    #single_true_kpis = None
    single_result = {
        "Scope 1" : [],
        "Scope 2" : [],
        "Scope 3" : [],
    }

    def __init__(self,ouput_path) -> None:
        self.output_path = ouput_path

    def evaluate(self,true_dict,expec_pd) -> None: 
        self.true_dict = true_dict
        self.expec_pd = expec_pd

        self.cnt += 1
    
        self.classify()
        self.aggregate_Scope()
        self.aggregate_Total()

    def classify(self) -> None:

        for key,value in self.true_dict.items():

            id = value.get("ID")
            
            for (y, v, p) in zip(value.get("Year"),value.get("Value"), value.get("Page")):
                df = self.expec_pd.copy()
                filtered_df = df[
                    (df["KPI_ID"] == int(id) ) &
                    (df["YEAR"] == int(y) ) &
                    (df["PAGE_NUM"] == int(p) ) &
                    (df["VALUE"] == v )
                ]    
                if len(filtered_df) == 1: 
                    self.single_result[key].append(True)
                else:
                    self.single_result[key].append(False)

    
    def aggregate_Scope(self) -> None:
        # calculate average by formula hat_{V}_N+1  = hat_{V}_N + a_N+1(V_N+1-hat_{V}_N ) 
        for key,value in self.single_result.items():
            v_N1 = self.mean(value)
            hat_v_N = self.scope_accuracy.get(key)
            self.scope_accuracy[key] = hat_v_N  + (1/self.cnt)*(v_N1-hat_v_N)

    def aggregate_Total(self) -> None:
        # calculate average by formula hat_{V}_N+1  = hat_{V}_N + a_N+1(V_N+1-hat_{V}_N ) 
        v_N1 = 0
        for value in self.scope_accuracy.values():
            v_N1 += value
        v_N1 = (v_N1/len(self.scope_accuracy))
        hat_v_N = self.total_accuracy
        self.total_accuracy = hat_v_N  + (1/self.cnt)*(v_N1-hat_v_N)

    

    def mean(self,bool_list) -> float:
        # Check if the list is not empty to avoid division by zero
        if len(bool_list) == 0:
            return None  # You may choose to handle this case differently based on your requirements
        else:
            # Calculate the mean (proportion of True values)
            mean_value = sum(bool_list) / len(bool_list)
            return mean_value


    def output_result(self):
        


        data = [
                    [
                        'Total Accuracy','Scope 1','Scope 2','Scope 3', 'No. of Tests'
                    ],
                    [
                        self.total_accuracy,
                        self.scope_accuracy["Scope 1"],
                        self.scope_accuracy["Scope 2"],
                        self.scope_accuracy["Scope 3"],
                        self.cnt
                    ]
                ]
        
        logging.debug(f"Total Accuracy: '{data[1][0]}")
        logging.debug(f"Scope 1: '{data[1][1]}")
        logging.debug(f"Scope 2: '{data[1][2]}")
        logging.debug(f"Scope 3: '{data[1][3]}")
        logging.debug(f"Comparisons between Expected and True: '{data[1][4]}")

        csv_path = os.path.join(self.output_path,"accuracy.csv")

        with open(csv_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write the data to the CSV file
                csv_writer.writerows(data)
        logging.debug(f"CSV File '{csv_path}' has been successfully generated!")        



            


     