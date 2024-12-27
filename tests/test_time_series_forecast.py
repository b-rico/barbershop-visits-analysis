"""
File Name: test_time_series_forecast.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the time_series_forecast function in the time_series_forecast.py script.
"""

import unittest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tempfile
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from scripts.time_series_forecast import time_series_forecast


class TestTimeSeriesForecast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create mock daily data for visits and revenue over ~60 days.
        """
        start_date = datetime(2023, 1, 1)
        num_days = 60

        dates = [start_date + timedelta(days=i) for i in range(num_days)]
        daily_visits_counts = np.random.randint(0, 6, size=num_days)
        
        rows = []
        for d, visits in zip(dates, daily_visits_counts):
            for _ in range(visits):
                rows.append({
                    'date': d,
                    'revenue': float(np.random.choice([15, 20, 25, 30, 35, 40, 45, 50])),
                })
        cls.mock_data = pd.DataFrame(rows)

    def test_time_series_forecast(self):
        """
        Tests the time_series_forecast function:
        1) Ensures the output CSV files are created.
        2) Checks that the CSVs have forecast columns (yhat, yhat_lower, yhat_upper).
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            time_series_forecast(self.mock_data, output_dir=tmp_dir, forecast_days=14)

            visit_forecast_path = os.path.join(tmp_dir, "visit_forecast.csv")
            revenue_forecast_path = os.path.join(tmp_dir, "revenue_forecast.csv")

            self.assertTrue(os.path.exists(visit_forecast_path), "visit_forecast.csv was not created.")
            self.assertTrue(os.path.exists(revenue_forecast_path), "revenue_forecast.csv was not created.")

            visit_df = pd.read_csv(visit_forecast_path)
            revenue_df = pd.read_csv(revenue_forecast_path)

            for col in ["ds", "yhat", "yhat_lower", "yhat_upper"]:
                self.assertIn(col, visit_df.columns, f"Column '{col}' missing in visit_forecast.csv")
                self.assertIn(col, revenue_df.columns, f"Column '{col}' missing in revenue_forecast.csv")

            unique_dates_in_mock = self.mock_data["date"].dt.date.unique()
            self.assertGreater(len(visit_df), len(unique_dates_in_mock), "visit_forecast.csv has no future rows.")
            self.assertGreater(len(revenue_df), len(unique_dates_in_mock), "revenue_forecast.csv has no future rows.")

if __name__ == '__main__':
    unittest.main()
