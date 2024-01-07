# ============================================================================================================================
# main_evaluation.py
# File   : main_evaluation.py
# Author : Zakaria Jouahri
# Date   : 16.12.2023
# ============================================================================================================================
from TestEvaluation import TestEvaluation
from KPIResultSet import KPIResultSet
from globals import print_big
from test import load_test_data, test_prepare_kpi_specs


def evaluation():
    # Output 
    test_data = load_test_data(r'rule_based_pipeline/output/TEST_Deutsche Bank_2022_EN.pdf.csv')

    #test_data.filter_kpis(by_source_file=['T_Rowe_Price_2021_EN.pdf'])

    print_big("Data-set", False)
    print(test_data)

    # True / Expected Values 
    kpi_results = KPIResultSet.load_from_csv(r'rule_based_pipeline/output/Deutsche Bank_2022_EN.pdf.csv')
    print_big("Kpi-Results", do_wait=False)
    print(kpi_results)

    kpis = test_prepare_kpi_specs()

    print_big("Kpi-Evaluation", do_wait=False)
    test_eval = TestEvaluation.generate_evaluation(kpis, kpi_results, test_data)
    print(test_eval)


def main():
    evaluation()


# Entry point of the program
if __name__ == "__main__":
    main()
