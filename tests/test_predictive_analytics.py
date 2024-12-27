"""
File Name: test_predictive_analytics.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the predictive_analytics function in the predictive_analytics.py script.
"""

import unittest
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.predictive_analytics import predictive_analytics

class TestPredictiveAnalytics(unittest.TestCase):
    def setUp(self):
        # Prepare mock data
        self.data = pd.DataFrame({
            'id': [1, 1, 2, 2, 3],
            'date': ['2023-01-01', '2023-02-01', '2023-01-15', '2023-02-15', '2023-03-01']
        })
        self.data['date'] = pd.to_datetime(self.data['date'])

        # Expected results
        self.expected = pd.DataFrame({
            'id': [1, 2, 3],
            'last_visit_date': pd.to_datetime(['2023-02-01', '2023-02-15', '2023-03-01']),
            'predicted_next_visit': pd.to_datetime(['2023-03-01', '2023-03-15', None])  # Example predictions
        })

        self.output_dir = "./output_test"
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Cleanup the output directory
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)

    def test_predictive_analytics(self):
        # Run the function
        predictive_analytics(self.data, self.output_dir)

        # Check the output file
        output_file = os.path.join(self.output_dir, "predicted_next_visits.csv")
        self.assertTrue(os.path.exists(output_file), "Predicted visits output file not found.")

        # Load the results and validate accuracy
        results = pd.read_csv(output_file, parse_dates=['last_visit_date', 'predicted_next_visit'])
        merged = pd.merge(results, self.expected, on='id', suffixes=('_actual', '_expected'))

        # Check if the predicted dates are within acceptable limits (e.g., ±1 day tolerance)
        merged['accuracy'] = (merged['predicted_next_visit_actual'] == merged['predicted_next_visit_expected'])
        accuracy_score = merged['accuracy'].mean()

        # Ensure a high accuracy score (e.g., >90%)
        self.assertGreaterEqual(accuracy_score, 0.9, "Prediction accuracy is below 90%.")

        # Cleanup
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
