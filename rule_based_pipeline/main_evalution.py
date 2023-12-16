from rule_based_pipeline.TestEvaluation import TestEvaluation
from rule_based_pipeline.KPIResultSet import KPIResultSet
from rule_based_pipeline.globals import print_big
from rule_based_pipeline.test import load_test_data, test_prepare_kpi_specs


def evaluation():
    test_data = load_test_data(r'output_rule_based_pipeline/T_Rowe_Price_2021_EN.pdf.csv')

    test_data.filter_kpis(by_source_file=[
        'T_Rowe_Price_2021_EN.pdf'            # KPIs are on pg: 84: 2009:665.1 ... 2013:575.7
    ])

    print_big("Data-set", False)
    print(test_data)
    kpi_results = KPIResultSet.load_from_file(r'test_data/kpiresults_test_all_files_against_kpi_2_0.json')
    print_big("Kpi-Results", do_wait=False)
    print(kpi_results)
    print_big("Kpi-Evaluation", do_wait=False)
    kpis = test_prepare_kpi_specs()
    test_eval = TestEvaluation.generate_evaluation(kpis, None, test_data)
    print(test_eval)


def main():
    evaluation()


# Entry point of the program
if __name__ == "__main__":
    main()
