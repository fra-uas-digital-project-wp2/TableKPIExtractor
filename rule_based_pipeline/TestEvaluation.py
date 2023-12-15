# ============================================================================================================================
# PDF_Analyzer
# File   : TestEvaluation.py
# Author : Ismail Demir (G124272)
# Date   : 10.09.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable
from Format_Analyzer import Format_Analyzer
from globals import print_verbose


class TestEvaluation:
    EVAL_TRUE_POSITIVE = 0
    EVAL_FALSE_POSITIVE = 1
    EVAL_TRUE_NEGATIVE = 2
    EVAL_FALSE_NEGATIVE = 3

    class TestEvalSample:

        def __init__(self, kpi_spec, kpi_measure, test_sample, year, pdf_file_name):
            """
            Represents a sample for evaluating KPIs.

            Args:
                kpi_spec (KPI): The KPI specification.
                kpi_measure (KPIMeasure): The extracted KPI measure.
                test_sample (TestDataSample): The corresponding test data sample.
                year (int): The year associated with the sample.
                pdf_file_name (str): The name of the PDF file.
            """
            self.kpi_spec = kpi_spec
            self.kpi_measure = kpi_measure
            self.test_sample = test_sample
            self.year = year
            self.pdf_file_name = pdf_file_name

        def get_true_value(self):
            """
            Get the true value from the test sample.

            Returns:
                float: The true value or None if not applicable.
            """
            return None if self.test_sample is None else Format_Analyzer.to_float_number(self.test_sample.data_answer)

        def get_extracted_value(self):
            """
            Get the extracted value from the KPI measure.

            Returns:
                float: The extracted value or None if not applicable.
            """
            return None if self.kpi_measure is None else Format_Analyzer.to_float_number(self.kpi_measure.value)

        def eval(self):
            """
            Evaluate the match between true and extracted values.

            Returns:
                int: Evaluation code (True Positive, False Positive, True Negative, False Negative).
            """
            if self.kpi_measure is not None and self.test_sample is not None:
                if abs(self.get_extracted_value() - self.get_true_value()) < 0.0001:
                    return TestEvaluation.EVAL_TRUE_POSITIVE
                return TestEvaluation.EVAL_FALSE_POSITIVE

            if self.test_sample is not None:
                return TestEvaluation.EVAL_FALSE_NEGATIVE

            if self.kpi_measure is not None:
                return TestEvaluation.EVAL_FALSE_POSITIVE

            return TestEvaluation.EVAL_TRUE_NEGATIVE

        def eval_to_str(self):
            """
            Convert the evaluation result to a human-readable string.

            Returns:
                str: Human-readable evaluation result.
            """
            eval_id = self.eval()
            if eval_id == TestEvaluation.EVAL_TRUE_POSITIVE:
                return "True Positive"
            if eval_id == TestEvaluation.EVAL_FALSE_POSITIVE:
                return "False Positive"
            if eval_id == TestEvaluation.EVAL_TRUE_NEGATIVE:
                return "True Negative"
            if eval_id == TestEvaluation.EVAL_FALSE_NEGATIVE:
                return "False Negative"
            return "Unknown"

    def __init__(self):
        """
        Initialize a TestEvaluation instance.
        """
        self.eval_samples = []
        self.num_true_positive = 0
        self.num_false_positive = 0
        self.num_true_negative = 0
        self.num_false_negative = 0
        self.measure_precision = 0.0
        self.measure_recall = 0.0

    def do_evaluations(self):
        """
        Perform evaluations based on collected samples.
        """
        self.num_true_positive = 0
        self.num_false_positive = 0
        self.num_true_negative = 0
        self.num_false_negative = 0
        for e in self.eval_samples:
            eval_id = e.eval()
            if eval_id == TestEvaluation.EVAL_TRUE_POSITIVE:
                self.num_true_positive += 1
            if eval_id == TestEvaluation.EVAL_FALSE_POSITIVE:
                self.num_false_positive += 1
            if eval_id == TestEvaluation.EVAL_TRUE_NEGATIVE:
                self.num_true_negative += 1
            if eval_id == TestEvaluation.EVAL_FALSE_NEGATIVE:
                self.num_false_negative += 1

        if self.num_true_positive > 0:
            self.measure_precision = self.num_true_positive / float(self.num_true_positive + self.num_false_positive)
            self.measure_recall = self.num_true_positive / float(self.num_true_positive + self.num_false_negative)
        else:
            self.measure_precision = 0.0
            self.measure_recall = 0.0

    def to_string(self, max_width, min_col_width, format):
        """
        Convert the evaluation results to a formatted string.

        Args:
            max_width (int): Maximum width of the output string.
            min_col_width (int): Minimum width of each column.
            format (str): Output format (e.g., ConsoleTable.FORMAT_CSV).

        Returns:
            str: Formatted string representation of the evaluation results.
        """
        console_table = ConsoleTable(7)
        column_headers = [
            'KPI_ID', 'KPI_NAME', 'PDF_FILE', 'YEAR', 'TRUE VALUE', 'EXTRACTED VALUE', 'CLASSIFICATION'
        ]
        console_table.cells.extend(column_headers)

        for e in self.eval_samples:
            console_table.cells.extend([
                str(e.kpispec.kpi_id), str(e.kpispec.kpi_name), str(e.pdf_file_name),
                str(e.year), str(e.get_true_value()), str(e.get_extracted_value()),
                e.eval_to_str().upper()
            ])

        result = console_table.to_string(max_width, min_col_width, format)

        result += "\nSUMMARY:\n"
        result += "True Positives : " + str(self.num_true_positive) + "\n"
        result += "False Positives : " + str(self.num_false_positive) + "\n"
        result += "True Negatives : " + str(self.num_true_negative) + "\n"
        result += "False Negatives : " + str(self.num_false_negative) + "\n"
        result += "Precision : " + str(self.measure_precision) + "\n"
        result += "Recall : " + str(self.measure_recall) + "\n"

        return result

    def __repr__(self):
        """
        Return a string representation of the TestEvaluation.

        Returns:
            str: String representation of the TestEvaluation.
        """
        return self.to_string(120, 5, ConsoleTable.FORMAT_CSV)

    @staticmethod
    def generate_evaluation(kpi_specs, kpi_results, test_data):
        """
        Generate evaluation results for a set of KPI specifications, KPI results, and test data.

        Args:
            kpi_specs (list): List of KPI specifications.
            kpi_results (KPIResultSet): Results of the KPI analysis.
            test_data (TestData): Test data for evaluation.

        Returns:
            TestEvaluation: Evaluation results.
        """
        pdf_file_names = test_data.get_unique_list_of_pdf_files()
        res = TestEvaluation()

        for kpi_spec in kpi_specs:
            print_verbose(1,
                          'Evaluating KPI: kpi_id=' + str(kpi_spec.kpi_id) + ', kpi_name="' + kpi_spec.kpi_name + '"')
            for pdf_file_name in pdf_file_names:
                print_verbose(1, '--->> Evaluating PDF = "' + pdf_file_name + '"')

                # Find values in test data samples for this kpi/pdf:
                for s in test_data.samples:
                    if s.data_kpi_id == kpi_spec.kpi_id and s.fixed_source_file == pdf_file_name:
                        # match (True KPI exists in pdf)
                        cur_eval_sample = None
                        # are there any matches in our results?
                        for k in kpi_results.kpimeasures:
                            if k.kpi_id == kpi_spec.kpi_id and k.src_file == pdf_file_name and k.year == s.data_year:  # yes (Extracted KPI exists)
                                # yes (Extracted KPI exists)
                                cur_eval_sample = TestEvaluation.TestEvalSample(kpi_spec, k, s, k.year, pdf_file_name)
                                break
                        if cur_eval_sample is None:
                            # no
                            cur_eval_sample = TestEvaluation.TestEvalSample(kpi_spec, None, s, s.data_year,
                                                                            pdf_file_name)
                        res.eval_samples.append(cur_eval_sample)

                # Any unmatched kpi results (i.e. extracted KPIs) left?
                for k in kpi_results.kpimeasures:
                    if k.src_file != pdf_file_name:
                        continue
                    found = False
                    for e in res.eval_samples:
                        if e.kpi_measure is not None and k.kpi_id == e.kpi_spec.kpi_id and k.year == e.year and e.kpi_measure.src_file == pdf_file_name:
                            found = True
                            break
                    if not found:
                        # unmatched
                        cur_eval_sample = TestEvaluation.TestEvalSample(kpi_spec, k, None, k.year, pdf_file_name)
                        res.eval_samples.append(cur_eval_sample)

        res.do_evaluations()
        return res
