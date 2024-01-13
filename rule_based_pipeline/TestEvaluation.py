# ============================================================================================================================
# PDF_Analyzer
# File   : TestEvaluation.py
# Author : Ismail Demir (G124272)
# Date   : 10.09.2020
# ============================================================================================================================
from ConsoleTable import ConsoleTable
from FormatAnalyzer import FormatAnalyzer


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
                kpi_id (KPI): The KPI specification.
                kpi_name (KPIMeasure): The extracted KPI measure.
                pdf_file_name (str): The name of the PDF file.
                year (int): The year associated with the sample.
                actual_value (TestDataSample): The corresponding test data sample.
                expected_value (TestDataSample): The corresponding test data sample.
            """
            self.kpi_id = kpi_id
            self.kpi_name = kpi_name
            self.pdf_file_name = pdf_file_name
            self.year = year
            self.actual_value = actual_value
            self.expected_value = expected_value

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
    def generate_evaluation(pdf_file_name, expected_values, actual_values):
        """
        Generate evaluation results for a set of KPI results, and test data.

        Args:
            pdf_file_name (str): The name of the PDF file.
            expected_values (KPIResultSet): Results of the KPI analysis.
            actual_values (TestData): Test data for evaluation
        Returns:
            TestEvaluation: Evaluation results.
        """
        # Initialize TestEvaluation object to store evaluation results
        results = TestEvaluation()

        # Iterate through each actual value
        for sample in actual_values.samples:
            # Initialize actual variables
            actual_kpi_id = int(sample.kpi_id)
            actual_kpi_name = sample.kpi_name
            actual_year = int(sample.year)
            actual_value = sample.value
            actual_value_exists_in_expected_values = False

            # Iterate through each expected value
            for expected_value_measure in expected_values.kpi_measures:
                # Initialize expected variables
                expected_kpi_id = int(expected_value_measure.kpi_id)
                expected_year = int(expected_value_measure.year)
                expected_value = FormatAnalyzer.to_float_number(expected_value_measure.value)

                # Check if the KPI ID and year match between actual and expected values
                if actual_kpi_id == expected_kpi_id and actual_year == expected_year:
                    # Remove Matched Value from Expected Values:
                    expected_values.kpi_measures.remove(expected_value_measure)

                    # Match (Extracted KPI exists)
                    cur_eval_sample = TestEvaluation.TestEvalSample(actual_kpi_id, actual_kpi_name, pdf_file_name,
                                                                    actual_year, actual_value, expected_value)
                    results.eval_samples.append(cur_eval_sample)

                    # Set flag Match Existence and break
                    actual_value_exists_in_expected_values = True
                    break

            # If no match found for the current actual value, add it as False Negative
            if not actual_value_exists_in_expected_values:
                cur_eval_sample = TestEvaluation.TestEvalSample(actual_kpi_id, actual_kpi_name, pdf_file_name,
                                                                actual_year, actual_value, None)
                results.eval_samples.append(cur_eval_sample)

        # Add any remaining expected values as False Positive
        if len(expected_values.kpi_measures) > 0:
            for remaining_kpi_measure in expected_values.kpi_measures:
                # Initialize remaining variables
                kpi_id = int(remaining_kpi_measure.kpi_id)
                kpi_name = remaining_kpi_measure.kpi_name
                year = int(remaining_kpi_measure.year)
                value = FormatAnalyzer.to_float_number(remaining_kpi_measure.value)

                cur_eval_sample = TestEvaluation.TestEvalSample(kpi_id, kpi_name, pdf_file_name, year, None, value)
                results.eval_samples.append(cur_eval_sample)

        # Perform evaluations based on collected samples
        results.do_evaluations()

        # Return the final evaluation results
        return results
