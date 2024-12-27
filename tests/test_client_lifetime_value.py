"""
File Name: test_client_lifetime_value.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains the main function that calls the client_lifetime_value function.
"""

import unittest
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from scripts.client_lifetime_value import client_lifetime_value

class TestClientLifetimeValue(unittest.TestCase):
    def test_client_lifetime_value(self):
        data = pd.DataFrame({
            'id': [1, 1, 2, 2, 3],
            'date': ['2023-01-01', '2023-07-01', '2022-12-01', '2023-01-15', '2023-07-15']
        })
        data['date'] = pd.to_datetime(data['date'])

        output_dir = "./output_test"
        os.makedirs(output_dir, exist_ok=True)

        client_lifetime_value(data, output_dir, avg_revenue_per_visit=50)

        output_file = os.path.join(output_dir, "client_lifetime_value.csv")
        self.assertTrue(os.path.exists(output_file), "Output file not found.")

        os.remove(output_file)
        os.rmdir(output_dir)

if __name__ == '__main__':
    unittest.main()

