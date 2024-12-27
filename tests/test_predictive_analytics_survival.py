"""
File Name: test_predictive_analytics_survival.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the predictive_analytics_survival functions in the predictive_analytics_survival.py script.
"""
"""
File Name: test_predictive_analytics.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This file contains unit tests for the predictive_analytics function in the predictive_analytics.py script.
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
from scripts.predictive_analytics_survival import (
    create_survival_dataset_from_df,
    fit_cox_model,
    predict_next_visit,
    predictive_analytics_survival_df
)

class TestPredictiveAnalyticsSurvival(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Create a mock DataFrame (cls.mock_data) representing visits:
        - 5 clients
        - Random visit dates over ~60 days
        - Random revenue per visit
        """
        np.random.seed(42)
        rows = []
        num_clients = 5
        start_date = datetime(2023, 1, 1)

        for client_id in range(1, num_clients + 1):
            visit_count = np.random.randint(3, 9)
            current_date = start_date

            for _ in range(visit_count):
                rows.append({
                    'id': client_id,
                    'date': current_date,
                    'revenue': float(np.random.choice([15, 20, 25, 30, 35, 40, 45, 50])),
                })
                current_date += timedelta(days=np.random.randint(1, 15))

        cls.mock_data = pd.DataFrame(rows)
    
    def test_create_survival_dataset_from_df(self):
        """
        Tests the creation of a survival dataset from the mock visits DataFrame.
        Ensures that 'duration' and 'event' columns are created as expected.
        """
        survival_df = create_survival_dataset_from_df(self.mock_data)

        self.assertFalse(survival_df.empty, "Survival dataset is unexpectedly empty.")

        expected_cols = ['id', 'start', 'stop', 'duration', 'event', 'revenue_feature']
        for col in expected_cols:
            self.assertIn(col, survival_df.columns, f"'{col}' column is missing in survival dataset.")

        self.assertTrue(pd.api.types.is_numeric_dtype(survival_df['duration']), 
                        "duration must be numeric.")
        event_values = set(survival_df['event'].unique())
        self.assertTrue(event_values.issubset({0, 1}), 
                        f"event column contains values other than 0/1: {event_values}")

    def test_fit_cox_model(self):
        """
        Tests if a Cox model can be fit without error on the survival dataset.
        """
        survival_df = create_survival_dataset_from_df(self.mock_data)
        model = fit_cox_model(survival_df)
        self.assertIsNotNone(model, "CoxPHSurvivalAnalysis model is None.")
    
    def test_predict_next_visit(self):
        """
        Tests prediction of the next visit date for a single client scenario.
        """
        survival_df = create_survival_dataset_from_df(self.mock_data)
        model = fit_cox_model(survival_df)

        random_row = self.mock_data.sample(1).iloc[0]
        current_date = random_row['date']
        revenue_feature = random_row['revenue']

        next_visit = predict_next_visit(
            cox_model=model,
            current_date=current_date,
            revenue_feature=revenue_feature,
            max_days=30,
            threshold=0.5
        )

        self.assertTrue(
            (next_visit is None) or isinstance(next_visit, pd.Timestamp), 
            f"predict_next_visit returned unexpected type: {type(next_visit)}"
        )

    def test_predictive_analytics_survival_df(self):
        """
        End-to-end test:
        1) Runs the survival analysis pipeline on mock data.
        2) Ensures the output CSV is created with expected columns.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            predictive_analytics_survival_df(self.mock_data, output_dir=tmpdir)
            
            output_csv = os.path.join(tmpdir, "predicted_next_visits_survival.csv")
            self.assertTrue(os.path.exists(output_csv), "Output CSV file was not created.")

            results_df = pd.read_csv(output_csv)
            for col in ['id', 'last_visit_date', 'predicted_next_visit']:
                self.assertIn(col, results_df.columns, f"'{col}' column missing in output CSV.")

if __name__ == '__main__':
    unittest.main()
