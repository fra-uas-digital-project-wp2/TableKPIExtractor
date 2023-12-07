import json
class KPIResultSetTrue:
    
    cnt = 0

    json_directory = None
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


    def __init__(self,json_directory) -> None:
        self.json_directory = json_directory
        

    def load(self,json_name) -> None:
        self.true_kpis_dict = json.load(open(self.json_directory+json_name[0:-4]+".json"))

    def evaluate(self,kpiresults) -> None: 
        self.cnt += 1
        self.classify(kpiresults)
        self.aggregate_Scope()
        self.aggregate_Total()

    def classify(self,kpiresults) -> None:

        for key,value in self.true_kpis_dict.items():
            for (y, v, p) in zip(value.get("Year"),value.get("Value"), value.get("Page")):
                for kpiresult in kpiresults:
                    if (value.get("ID") != kpiresult.kpi_id) or (y != kpiresult.year):
                        continue
                    if (str(v) == kpiresult.value) and (p == kpiresult.page_num):
                        self.single_result[key].append(True)
                        kpiresult.correct = True
                    else:
                        self.single_result[key].append(False)
                        kpiresult.correct = False
    
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


    def printEval(self):
        print("Total Accuracy: ")

        print(self.total_accuracy)

        print("Scope Accuracy: ")

        print(self.scope_accuracy)

        print("Single Result")

        print(self.single_result)


            


     