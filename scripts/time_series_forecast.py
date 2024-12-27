"""
File Name: time_series_forecast.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This function forecasts the daily visits and daily revenue for a specified number of future days
    using Facebook/Meta Prophet.
Args:
    - data (DataFrame): The DataFrame containing at least 'date' and 'revenue' columns.
                        Each row represents one visit. 'date' should be in datetime format.
    - output_dir (str): The directory where forecast CSV files will be saved.
    - forecast_days (int): The number of days into the future to forecast (default=30).
Output:
    - Two CSV files saved in 'output_dir':
        1) 'visit_forecast.csv': Contains the forecasted daily visits with columns
        2) 'revenue_forecast.csv': Contains the forecasted daily revenue with columns
"""

import pandas as pd
import os

# Prophet can be imported as follows:
from prophet import Prophet

def time_series_forecast(data, output_dir, forecast_days=30):
    """
    This function forecasts the daily visits and daily revenue for a specified 
    number of future days using Facebook/Meta Prophet.

    Args:
    - data (DataFrame): The DataFrame containing at least 'date' and 'revenue' columns.
                        Each row represents one visit. 'date' should be in datetime format.
    - output_dir (str): The directory where forecast CSV files will be saved.
    - forecast_days (int): The number of days into the future to forecast (default=30).

    Outputs:
    - Two CSV files saved in 'output_dir':
        1) 'visit_forecast.csv': Contains the forecasted daily visits with columns
           ['ds', 'yhat', 'yhat_lower', 'yhat_upper', ...].
        2) 'revenue_forecast.csv': Contains the forecasted daily revenue with columns
           ['ds', 'yhat', 'yhat_lower', 'yhat_upper', ...].
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # 1) Aggregate data by date to get daily visits & daily revenue
    data['date'] = pd.to_datetime(data['date'])
    
    # Daily visits: group by date, count rows
    daily_visits = (data
                    .groupby(data['date'].dt.date)  # group by just the date part (no time)
                    .size()
                    .reset_index(name='visits'))

    # Convert date column to datetime (Prophet expects 'ds' and 'y' columns)
    daily_visits['ds'] = pd.to_datetime(daily_visits['date'])
    daily_visits['y'] = daily_visits['visits']
    daily_visits = daily_visits[['ds', 'y']]  # Prophet naming convention

    # Daily revenue: group by date, sum revenue
    daily_revenue = (data
                     .groupby(data['date'].dt.date)['revenue']
                     .sum()
                     .reset_index(name='total_revenue'))

    # Convert date column to datetime
    daily_revenue['ds'] = pd.to_datetime(daily_revenue['date'])
    daily_revenue['y'] = daily_revenue['total_revenue']
    daily_revenue = daily_revenue[['ds', 'y']]

    # 2) Forecast Daily Visits with Prophet
    visits_model = Prophet(
        yearly_seasonality=True, 
        weekly_seasonality=True, 
        daily_seasonality=False  # Depending on your data
    )
    visits_model.fit(daily_visits)

    # Create a future DataFrame of forecast_days
    future_visits = visits_model.make_future_dataframe(periods=forecast_days)
    visits_forecast = visits_model.predict(future_visits)

    # Save the visits forecast to CSV
    visits_forecast.to_csv(os.path.join(output_dir, 'visit_forecast.csv'), index=False)

    # 3) Forecast Daily Revenue with Prophet
    revenue_model = Prophet(
        yearly_seasonality=True, 
        weekly_seasonality=True, 
        daily_seasonality=False
    )
    revenue_model.fit(daily_revenue)

    # Create a future DataFrame
    future_revenue = revenue_model.make_future_dataframe(periods=forecast_days)
    revenue_forecast = revenue_model.predict(future_revenue)

    # Save the revenue forecast to CSV
    revenue_forecast.to_csv(os.path.join(output_dir, 'revenue_forecast.csv'), index=False)

    # 4) Print success messages
    print(f"Time-series forecast complete for the next {forecast_days} days.")
    print(f"Visit forecast saved to:   {os.path.join(output_dir, 'visit_forecast.csv')}")
    print(f"Revenue forecast saved to: {os.path.join(output_dir, 'revenue_forecast.csv')}")
