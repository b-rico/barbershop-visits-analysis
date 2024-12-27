"""
File Name: test_trend_analysis.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the trend_analysis function in the trend_analysis.py script.
"""

import unittest
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.trend_analysis import trend_analysis

class TestTrendAnalysis(unittest.TestCase):
    def test_trend_analysis(self):
        data = pd.DataFrame({
            'id': [1, 1, 2, 2, 3],
            'date': ['2023-01-01', '2023-07-01', '2022-12-01', '2023-01-15', '2023-07-15']
        })
        data['date'] = pd.to_datetime(data['date'])

        output_dir = "./output_test"
        os.makedirs(output_dir, exist_ok=True)

        trend_analysis(data, output_dir)

        output_file = os.path.join(output_dir, "monthly_visits_trend.csv")
        self.assertTrue(os.path.exists(output_file), "Output file not found.")

        os.remove(output_file)
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()
