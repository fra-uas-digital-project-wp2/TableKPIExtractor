# ============================================================================================================================
# main_evaluation.py
# File   : main_evaluation.py
# Author : Zakaria Jouahri
# Date   : 16.12.2023
# ============================================================================================================================
from TestEvaluation import TestEvaluation
from KPIResultSet import KPIResultSet
from globals import print_big
from TestData import TestData


def load_actual_values_from_csv(file_path):
    actual_values = TestData()
    actual_values.load_from_csv(file_path)
    return actual_values


def evaluation():
    pdf_file_name = "Deutsche Bank_2018_EN.pdf.csv"

    # Output
    actual_values = load_actual_values_from_csv(r'output/' + pdf_file_name)

    print_big("Data-set", False)
    print(actual_values)

    # True / Expected Values
    expected_values = KPIResultSet.load_from_csv(r'output/Deutsche Bank_2018_EN.pdf_3.csv')
    print_big("Kpi-Results", do_wait=False)
    print(expected_values)

    print_big("Kpi-Evaluation", do_wait=False)
    test_eval = TestEvaluation.generate_evaluation(pdf_file_name, expected_values, actual_values)
    print(test_eval)


def main():
    evaluation()


# Entry point of the program
if __name__ == "__main__":
    main()
