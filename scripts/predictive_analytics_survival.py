"""
File Name: predictive_analytics_survival.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This script performs predictive analytics for next-visit forecasting using survival analysis.
    It predicts the next visit date for each client based on their visit history and revenue data.
    
    The script uses the sksurv library for survival analysis and Cox Proportional Hazards modeling.
    The main functions include:
    - create_survival_dataset_from_df: Converts a DataFrame of visits data into a survival dataset.
    - fit_cox_model: Trains a Cox Proportional Hazards model on the survival dataset.
    - predict_next_visit: Predicts the next visit date for a single client based on the Cox model.
    - predictive_analytics_survival_df: Performs predictive analytics and saves the results to a CSV file.
Args:
    - df (DataFrame): The raw visits DataFrame containing 'id', 'date', and 'revenue' columns.
    - output_dir (str): The directory where the output CSV file will be saved.
Output:
    - A CSV file named 'predicted_next_visits_survival.csv' saved to the specified output directory.
"""

import pandas as pd
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.util import Surv
import numpy as np
from datetime import timedelta
import os

def create_survival_dataset_from_df(df):
    """
    Transforms a DataFrame of visits data into a survival-analysis-friendly format
    by creating intervals for each client between consecutive visits.

    For each client ('id'), this function:
    - Sorts visits by date.
    - Creates start-stop intervals between consecutive visit dates.
    - Calculates the time interval (in days) between visits as the 'duration'.
    - Sets an 'event' indicator of 1 for intervals leading to another visit.
    - Marks the final visit in each client's history as censored (event=0).

    Args:
        df (DataFrame): A DataFrame with columns 'id', 'date', and 'revenue' (at minimum).
                        'date' should be in a datetime-compatible format.

    Returns:
        DataFrame: A new DataFrame containing rows of survival intervals with columns:
            - 'id': The client identifier.
            - 'start': The start visit date of the interval.
            - 'stop': The stop visit date of the interval (or same as 'start' if censored).
            - 'duration': Number of days between 'start' and 'stop'.
            - 'event': 1 if the interval ended with another visit, 0 if censored.
            - 'revenue_feature': The revenue feature (or other features) associated with
                                the start visit.
    """
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['id', 'date'])
    
    rows = []
    for customer_id, group in df.groupby('id'):
        group = group.sort_values('date')
        dates = group['date'].values
        revenues = group['revenue'].values
        
        for i in range(len(dates) - 1):
            start_date = dates[i]
            stop_date  = dates[i + 1]
            duration_days = int((stop_date - start_date) / np.timedelta64(1, 'D'))
            event = 1
            feature_revenue = revenues[i]
            rows.append({
                'id': customer_id,
                'start': start_date,
                'stop': stop_date,
                'duration': duration_days,
                'event': event,
                'revenue_feature': feature_revenue
            })
            
        if len(dates) > 0:
            i_last = len(dates) - 1
            start_date = dates[i_last]
            duration_days = 0
            event = 0
            feature_revenue = revenues[i_last]
            rows.append({
                'id': customer_id,
                'start': start_date,
                'stop': start_date,
                'duration': duration_days,
                'event': event,
                'revenue_feature': feature_revenue
            })
            
    survival_df = pd.DataFrame(rows)
    return survival_df

def fit_cox_model(survival_df):
    """
    Fits a Cox Proportional Hazards model to the provided survival dataset.

    This function:
    - Converts 'duration' and 'event' columns into a format suitable for survival modeling.
    - Creates a feature matrix from specified columns (e.g., 'revenue_feature').
    - Trains a CoxPHSurvivalAnalysis model.

    Args:
        survival_df (DataFrame): The survival dataset with columns:
                                ['duration', 'event', 'revenue_feature', ...].
                                'duration' is time in days, 'event' is 0/1.

    Returns:
        CoxPHSurvivalAnalysis: A fitted Cox Proportional Hazards model ready for predictions.
    """ 
    y = Surv.from_arrays(
        event=survival_df['event'].astype(bool),
        time=survival_df['duration'].values
    )
    X = survival_df[['revenue_feature']].copy()
    
    cox_model = CoxPHSurvivalAnalysis()
    cox_model.fit(X, y)
    return cox_model

def predict_next_visit(cox_model, current_date, revenue_feature, max_days=180, threshold=0.5):
    """
    Predicts the approximate next visit date for a single client state based on a Cox model.

    This function:
    - Evaluates the survival function for the provided feature vector (e.g., 'revenue_feature').
    - Looks over a range of days in the future (1 to max_days) to find the first day
      where the survival probability (probability of no visit) drops below a given threshold.
    - Interprets that day as the likely next visit date (i.e., a > (1 - threshold) chance
      that a visit occurs by that day).

    Args:
        cox_model (CoxPHSurvivalAnalysis): The trained Cox model for hazard/survival predictions.
        current_date (datetime): The date of the most recent known visit for this client.
        revenue_feature (float or int): The revenue feature (or other relevant numeric feature)
                                        used as input to the Cox model.
        max_days (int): The maximum range of days to check into the future (default: 180).
        threshold (float): The survival probability cutoff (default: 0.5). If survival
                           drops below this, we assume the visit has likely occurred.

    Returns:
        datetime or None: The predicted date of next visit. If the survival function never
                          drops below `threshold` within `max_days`, returns None.
    """ 
    X_test = pd.DataFrame({'revenue_feature': [revenue_feature]})
    
    surv_fn = cox_model.predict_survival_function(X_test)

    domain_min, domain_max = surv_fn[0].domain

    last_day = min(max_days, int(domain_max))
    if last_day < 1:
        return None

    times = np.arange(1, last_day + 1)

    sf = surv_fn[0](times)

    below_threshold = np.where(sf < threshold)[0]
    if len(below_threshold) > 0:
        predicted_days = int(below_threshold[0] + 1)
        return current_date + timedelta(days=predicted_days)
    else:
        return None



def predictive_analytics_survival_df(df, output_dir):
    """
    Performs predictive analytics for next-visit forecasting using survival analysis.

    This function:
    1) Converts the raw visits DataFrame into a survival analysis dataset via 
       `create_survival_dataset_from_df()`.
    2) Trains a Cox Proportional Hazards model with `fit_cox_model()`.
    3) For each client's last known visit, predicts the next likely visit date
       with `predict_next_visit()`.
    4) Saves a CSV file containing [id, last_visit_date, predicted_next_visit] for
       each client to the specified output directory.

    Args:
        df (DataFrame): The raw visits DataFrame containing at least 'id', 'date', and 'revenue'.
        output_dir (str): The path to the directory where the result CSV file will be saved.

    Output:
        - A CSV file named 'predicted_next_visits_survival.csv' is saved to `output_dir`.
    """
    survival_df = create_survival_dataset_from_df(df)
    cox_model = fit_cox_model(survival_df)

    results = []
    for customer_id, group in df.groupby('id'):
        group = group.sort_values('date')
        last_row = group.iloc[-1]
        last_visit_date = last_row['date']
        last_revenue = last_row['revenue']
        
        predicted_date = predict_next_visit(
            cox_model,
            current_date=last_visit_date,
            revenue_feature=last_revenue,
            max_days=180,
            threshold=0.5
        )
        
        results.append({
            'id': customer_id,
            'last_visit_date': last_visit_date,
            'predicted_next_visit': predicted_date
        })

    results_df = pd.DataFrame(results)

    results_df[['id', 'last_visit_date', 'predicted_next_visit']].to_csv(
        f"{output_dir}/predicted_next_visits_survival.csv", 
        index=False
    )
    print("Predictive Analytics Survival complete: predicted_next_visits_survival.csv generated.")
