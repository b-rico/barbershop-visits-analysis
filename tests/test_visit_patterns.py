"""
File Name: test_visit_patterns.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the visit_patterns function in the visit_patterns.py script.
"""

import unittest
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.visit_patterns import visit_patterns

class TestVisitPatterns(unittest.TestCase):
    def test_visit_patterns(self):
        data = pd.DataFrame({
            'id': [1, 1, 2, 2, 3],
            'date': ['2023-01-01', '2023-07-01', '2022-12-01', '2023-01-15', '2023-07-15']
        })
        data['date'] = pd.to_datetime(data['date'])

        output_dir = "./output_test"
        os.makedirs(output_dir, exist_ok=True)

        visit_patterns(data, output_dir)

        output_file1 = os.path.join(output_dir, "day_of_week_patterns.csv")
        output_file2 = os.path.join(output_dir, "month_patterns.csv")
        self.assertTrue(os.path.exists(output_file1), "Day of week patterns file not found.")
        self.assertTrue(os.path.exists(output_file2), "Month patterns file not found.")

        os.remove(output_file1)
        os.remove(output_file2)
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()
