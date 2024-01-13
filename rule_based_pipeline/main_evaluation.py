# ============================================================================================================================
# main_evaluation.py
# File   : main_evaluation.py
# Author : Zakaria Jouahri
# Date   : 16.12.2023
# ============================================================================================================================
from TestEvaluation import TestEvaluation
from KPIResultSet import KPIResultSet
from globals import print_big
from PreparationOfKPISpecs import prepare_kpi_specs
from TestData import TestData


def load_test_data(test_data_file_path):
    test_data = TestData()
    test_data.load_from_csv(test_data_file_path)
    return test_data


def evaluation():
    # Output
    actual_values = load_test_data(r'output/0_Deutsche Bank_2022_EN.pdf.csv')

    # output.filter_kpis(by_source_file=['T_Rowe_Price_2021_EN.pdf'])

    print_big("Data-set", False)
    print(actual_values)

    # True / Expected Values
    expected_values = KPIResultSet.load_from_csv(r'output/0_Deutsche Bank_2022_EN.pdf.csv')
    print_big("Kpi-Results", do_wait=False)
    print(expected_values)

    kpis = prepare_kpi_specs()

    print_big("Kpi-Evaluation", do_wait=False)
    test_eval = TestEvaluation.generate_evaluation(expected_values, actual_values)
    print(test_eval)


def main():
    evaluation()


# Entry point of the program
if __name__ == "__main__":
    main()
