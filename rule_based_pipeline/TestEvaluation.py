# ============================================================================================================================
# PDF_Analyzer
# File   : TestEvaluation.py
# Author : Ismail Demir (G124272)
# Date   : 10.09.2020
# ============================================================================================================================
import os
import config_for_rb

from ConsoleTable import ConsoleTable
from FormatAnalyzer import FormatAnalyzer


class TestEvaluation:
    # Constants for evaluation codes
    EVAL_TRUE_POSITIVE = 0
    EVAL_FALSE_POSITIVE = 1
    EVAL_TRUE_NEGATIVE = 2
    EVAL_FALSE_NEGATIVE = 3

    def __init__(self):
        """
        Initialize a TestEvaluation instance.
        """
        # List to store evaluation samples
        self.eval_samples = []

        # Initialize counters for evaluation metrics
        self.num_true_positive = 0
        self.num_false_positive = 0
        self.num_true_negative = 0
        self.num_false_negative = 0
        self.measure_precision = 0.0
        self.measure_recall = 0.0
        self.measure_accuracy = 0.0

    def do_evaluations(self):
        """
        Perform evaluations based on collected samples.

        Updates the evaluation metrics including true positives, false positives, true negatives, false negatives,
        precision, and recall.
        """
        # Initialize evaluation counters
        self.num_true_positive = 0
        self.num_false_positive = 0
        self.num_true_negative = 0
        self.num_false_negative = 0

        # Iterate through collected samples
        for sample in self.eval_samples:
            actual_value = sample['actual_value']
            expected_value = sample['expected_value']
            eval_id = self.eval(actual_value, expected_value)

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
            
        # Calculate accuracy
        if self.num_true_positive > 0 or self.num_true_negative > 0:
            self.measure_accuracy = (self.num_true_positive + self.num_true_negative) / float(self.num_true_positive + self.num_true_negative  + self.num_false_positive + self.num_false_negative)





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
        for sample in self.eval_samples:
            console_table.cells.extend([
                str(sample['kpi_id']), str(sample['kpi_name']), str(sample['pdf_file_name']),
                str(sample['year']), str(sample['actual_value']), str(sample['expected_value']),
                self.eval_to_str(sample['actual_value'], sample['expected_value']).upper()
            ])

        # Generate formatted string
        result = console_table.to_string(max_width, min_col_width, console_table_format)

        self.to_csv(result)

        # Reset Output String
        result = ""

        # Add summary information to the result string
        result += "\nSUMMARY:\n"
        result += "True Positives : " + str(self.num_true_positive) + "\n"
        result += "False Positives : " + str(self.num_false_positive) + "\n"
        result += "True Negatives : " + str(self.num_true_negative) + "\n"
        result += "False Negatives : " + str(self.num_false_negative) + "\n"
        result += "Precision : " + str(round(self.measure_precision,3)) + "\n"
        result += "Recall : " + str(round(self.measure_recall,3)) + "\n"
        result += "Accuracy : " + str(round(self.measure_accuracy,3)) + "\n"

        return result

    def eval_to_str(self, actual_value, expected_value):
        """
        Convert the evaluation result to a human-readable string.

        Returns:
            str: Human-readable evaluation result.
        """
        eval_id = self.eval(actual_value, expected_value)

        if eval_id == TestEvaluation.EVAL_TRUE_POSITIVE:
            return "True Positive"
        if eval_id == TestEvaluation.EVAL_FALSE_POSITIVE:
            return "False Positive"
        if eval_id == TestEvaluation.EVAL_TRUE_NEGATIVE:
            return "True Negative"
        if eval_id == TestEvaluation.EVAL_FALSE_NEGATIVE:
            return "False Negative"
        return "Unknown"

    def __repr__(self):
        """
        Return a string representation of the TestEvaluation.

        Returns:
            str: String representation of the TestEvaluation.
        """
        return self.to_string(120, 5, ConsoleTable.FORMAT_CSV)
    
    def to_csv(self,string):
        with open(os.path.join(config_for_rb.global_evaluation_results_folder,"evaluation_results.csv"), 'w') as file:
            # Write the string to the file
            file.write(string)

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
        for actual_value in actual_values.samples:
            # Set flag Match Existence to false
            actual_value_exists_in_expected_values = False

            # Iterate through each expected value
            for expected_value in expected_values.kpi_measures:
                # Check if the KPI ID and year match between actual and expected values
                if actual_value.kpi_id == expected_value.kpi_id and int(actual_value.year) == int(expected_value.year) and actual_value.src_file[:-4] == expected_value.src_file:
                    # Remove Matched Value from Expected Values
                    expected_values.kpi_measures.remove(expected_value)

                    # Match (Extracted KPI exists)
                    results.eval_samples.append({
                        'kpi_id': int(actual_value.kpi_id),
                        'kpi_name': actual_value.kpi_name,
                        'pdf_file_name': actual_value.src_file[:-4],
                        'year': int(actual_value.year),
                        'actual_value': actual_value.value,
                        'expected_value': FormatAnalyzer.to_float_number(expected_value.value)
                    })

                    # Set flag Match Existence and break
                    actual_value_exists_in_expected_values = True
                    break

            # If no match found for the current actual value, add it as False Negative
            if not actual_value_exists_in_expected_values:
                results.eval_samples.append({
                    'kpi_id': int(actual_value.kpi_id),
                    'kpi_name': actual_value.kpi_name,
                    'pdf_file_name': actual_value.src_file[:-4],
                    'year': int(actual_value.year),
                    'actual_value': actual_value.value,
                    'expected_value': None
                })

        # Add any remaining expected values as False Positive
        if len(expected_values.kpi_measures) > 0:
            for remaining_kpi_measure in expected_values.kpi_measures:
                results.eval_samples.append({
                    'kpi_id': int(remaining_kpi_measure.kpi_id),
                    'kpi_name': remaining_kpi_measure.kpi_name,
                    'pdf_file_name': remaining_kpi_measure.src_file,
                    'year': int(remaining_kpi_measure.year),
                    'actual_value': None,
                    'expected_value': FormatAnalyzer.to_float_number(remaining_kpi_measure.value)
                })

        # Perform evaluations based on collected samples
        results.do_evaluations()

        # Return the final evaluation results
        return results

    @staticmethod
    def eval(actual_value, expected_value):
        """
        Evaluate the match between expected (true) and actual (extracted) values.

        Returns:
            int: Evaluation code (True Positive, False Positive, True Negative, False Negative).
        """
        # Check if both actual_value and expected_value are not None
        if actual_value is not None and expected_value is not None:
            # Check if the values are equal
            if actual_value == expected_value:
                # Return True Positive if they are equal
                return TestEvaluation.EVAL_TRUE_POSITIVE
            # Return False Positive if they are not equal
            return TestEvaluation.EVAL_FALSE_POSITIVE

        # Check if there is an expected value but no actual value and return False Negative
        if expected_value is not None:
            return TestEvaluation.EVAL_FALSE_NEGATIVE

        # Check if there is an actual value but no expected value and return False Positive
        if actual_value is not None:
            return TestEvaluation.EVAL_FALSE_POSITIVE

        # Unreasonable won't happen in this setup, but if none of the above conditions are met, return True Negative
        return TestEvaluation.EVAL_TRUE_NEGATIVE
