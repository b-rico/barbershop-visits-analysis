"""
File Name: test_churn_analysis.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the churn_analysis function in the churn_analysis.py script.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.churn_analysis import churn_analysis
import unittest
import pandas as pd

class TestChurnAnalysis(unittest.TestCase):
    def test_churn_analysis(self):
        data = pd.DataFrame({
            'id': [1, 1, 2, 2],
            'date': ['2023-01-01', '2023-07-01', '2022-12-01', '2023-01-15']
        })
        data['date'] = pd.to_datetime(data['date'])

        output_dir = "./output_test"
        os.makedirs(output_dir, exist_ok=True)

        churn_analysis(data, output_dir, churn_threshold=180)

        output_file = os.path.join(output_dir, "churn_analysis.csv")
        self.assertTrue(os.path.exists(output_file), "Output file not found.")

        os.remove(output_file)
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()
