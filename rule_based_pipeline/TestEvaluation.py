# ============================================================================================================================
# PDF_Analyzer
# File   : TestEvaluation.py
# Author : Ismail Demir (G124272)
# Date   : 10.09.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable


class TestEvaluation:
    EVAL_TRUE_POSITIVE = 0
    EVAL_FALSE_POSITIVE = 1
    EVAL_TRUE_NEGATIVE = 2
    EVAL_FALSE_NEGATIVE = 3

    class TestEvalSample:
        def __init__(self, kpi_id, kpi_name, pdf_file_name, year, actual_value, expected_value):
            """
            Represents a sample for evaluating KPIs.

            Args:
                kpi_spec (KPI): The KPI specification.
                kpi_measure (KPIMeasure): The extracted KPI measure.
                test_sample (TestDataSample): The corresponding test data sample.
                year (int): The year associated with the sample.
                pdf_file_name (str): The name of the PDF file.
            """
            self.kpi_id = kpi_id
            self.kpi_name = kpi_name
            self.pdf_file_name = pdf_file_name
            self.year = year
            self.actual_value = actual_value
            self.expected_value = expected_value

        # def get_true_value(self):
        #     """
        #     Get the true value from the test sample.
        #
        #     Returns:
        #         float: The true value or None if not applicable.
        #     """
        #     return None if self.test_sample is None else self.test_sample.value
        #
        # def get_extracted_value(self):
        #     """
        #     Get the extracted value from the KPI measure.
        #
        #     Returns:
        #         float: The extracted value or None if not applicable.
        #     """
        #     return None if self.kpi_measure is None else FormatAnalyzer.to_float_number(self.kpi_measure.value)

        def eval(self):
            """
            Evaluate the match between true and extracted values.

            Returns:
                int: Evaluation code (True Positive, False Positive, True Negative, False Negative).
            """
            if self.actual_value is not None and self.expected_value is not None:

                # Check if the absolute difference between extracted and true values is below a threshold
                if self.actual_value == self.expected_value:
                    return TestEvaluation.EVAL_TRUE_POSITIVE
                return TestEvaluation.EVAL_FALSE_POSITIVE

            # No KPI measure, but there is a test sample (False Negative)
            if self.expected_value is not None:
                return TestEvaluation.EVAL_FALSE_NEGATIVE

            # No test sample, but there is a KPI measure (False Positive)
            if self.actual_value is not None:
                return TestEvaluation.EVAL_FALSE_POSITIVE

            # No KPI measure and no test sample (True Negative) // Unreasonable won't happen in this setup
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

        Updates the evaluation metrics including true positives, false positives,
        true negatives, false negatives, precision, and recall.
        """

        # Initialize evaluation counters
        self.num_true_positive = 0
        self.num_false_positive = 0
        self.num_true_negative = 0
        self.num_false_negative = 0

        # Iterate through collected samples
        for eval_sample in self.eval_samples:

            eval_id = eval_sample.eval()

            # Update counters based on evaluation results
            if eval_id == TestEvaluation.EVAL_TRUE_POSITIVE:
                self.num_true_positive += 1
            if eval_id == TestEvaluation.EVAL_FALSE_POSITIVE:
                self.num_false_positive += 1
            if eval_id == TestEvaluation.EVAL_TRUE_NEGATIVE:
                self.num_true_negative += 1
            if eval_id == TestEvaluation.EVAL_FALSE_NEGATIVE:
                self.num_false_negative += 1

        # Calculate precision and recall
        if self.num_true_positive > 0:
            self.measure_precision = self.num_true_positive / float(self.num_true_positive + self.num_false_positive)
            self.measure_recall = self.num_true_positive / float(self.num_true_positive + self.num_false_negative)
        else:
            self.measure_precision = 0.0
            self.measure_recall = 0.0

    def to_string(self, max_width, min_col_width, console_table_format):
        """
        Convert the evaluation results to a formatted string.

        Args:
            max_width (int): Maximum width of the output string.
            min_col_width (int): Minimum width of each column.
            console_table_format (str): Output format (e.g., ConsoleTable.FORMAT_CSV).

        Returns:
            str: Formatted string representation of the evaluation results.
        """

        # Initialize ConsoleTable for formatting
        console_table = ConsoleTable(7)

        # Define column headers
        column_headers = [
            'KPI_ID', 'KPI_NAME', 'PDF_FILE', 'YEAR', 'EXTRACTED VALUE', 'TRUE VALUE', 'CLASSIFICATION'
        ]
        console_table.cells.extend(column_headers)

        # Populate ConsoleTable with sample data
        for eval_sample in self.eval_samples:
            console_table.cells.extend([
                str(eval_sample.kpi_id), str(eval_sample.kpi_name), str(eval_sample.pdf_file_name),
                str(eval_sample.year), str(eval_sample.actual_value), str(eval_sample.expected_value),
                eval_sample.eval_to_str().upper()
            ])

        # Generate formatted string
        result = console_table.to_string(max_width, min_col_width, console_table_format)

        # Add summary information to the result string
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
    def generate_evaluation(expected_values, actual_values):
        """
        Generate evaluation results for a set of KPI specifications, KPI results, and test data.

        Args:
            expected_values (KPIResultSet): Results of the KPI analysis.
            actual_values (TestData): Test data for evaluation.

        Returns:
            TestEvaluation: Evaluation results.
        """

        # Get unique PDF file names from the test data
        exists = False
        pdf_file_name = actual_values.get_unique_list_of_pdf_files()

        # Initialize TestEvaluation object to store evaluation results
        results = TestEvaluation()
        # print(len(kpi_measure_control))
        # print(kpi_measure_control[0])
        # for kpi in kpi_measure_control:
        #     print(kpi)
        #     print(kpi.kpi_id)
        #     print(kpi.year)
        #     print(kpi.value)
        #     kpi_measure_control.remove(kpi)
        #     print(len(kpi_measure_control))
        # print("kpi_measure_control-----------------------------------------------")

        for actual_value in actual_values.samples:

            for expected_value in expected_values.kpi_measures:
                if str(actual_value.kpi_id) == str(expected_value.kpi_id) and str(actual_value.year) == str(expected_value.year):
                    print("Yes kpi_id and year")
                    # yes (Extracted KPI exists)
                    expected_values.kpi_measures.remove(expected_value)
                    cur_eval_sample = TestEvaluation.TestEvalSample(actual_value.kpi_id, actual_value.kpi_name, pdf_file_name, actual_value.year, actual_value.value, expected_value.value)
                    results.eval_samples.append(cur_eval_sample)
                    exists = True

                    if str(actual_value.raw_txt) == str(expected_value.value):
                        print("Yes value --- EVAL_TRUE_POSITIVE ")
                    else:
                        print("No value --- EVAL_FALSE_POSITIVE ")
                    break

                exists = False
            if not exists:
                print("EVAL_FALSE_POSITIVE")
                cur_eval_sample = TestEvaluation.TestEvalSample(actual_value.kpi_id, actual_value.kpi_name,pdf_file_name, actual_value.year,actual_value.value, None)
                results.eval_samples.append(cur_eval_sample)

        if len(expected_values.kpi_measures) > 0:
            for left_values in expected_values.kpi_measures:
                print("EVAL_FALSE_POSITIVE")
                cur_eval_sample = TestEvaluation.TestEvalSample(left_values.kpi_id, left_values.kpi_name,pdf_file_name, left_values.year,None, left_values)
                results.eval_samples.append(cur_eval_sample)

        results.do_evaluations()
        return results
