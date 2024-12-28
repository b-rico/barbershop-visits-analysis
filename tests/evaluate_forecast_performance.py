"""
evaluate_forecast_performance.py

This script demonstrates how to:
1) Split your data into a train/test set,
2) Train a Prophet model on the training set,
3) Generate a forecast for the test period,
4) Compare forecasted vs. actual values,
5) Calculate MAE and MSE.
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast_performance(data, date_col='ds', value_col='y',
                                  train_cutoff=None, forecast_days=30):
    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col)
    
    # If train_cutoff is a string, convert to datetime
    if isinstance(train_cutoff, str):
        train_cutoff = pd.to_datetime(train_cutoff)
    
    # If train_cutoff still None, pick last forecast_days as test
    if train_cutoff is None:
        max_date = df[date_col].max()
        train_cutoff = max_date - pd.Timedelta(days=forecast_days)

    train_df = df[df[date_col] <= train_cutoff].copy()
    test_df  = df[df[date_col] > train_cutoff].copy()

    if test_df.empty:
        raise ValueError("Test set is empty. Adjust 'train_cutoff' or 'forecast_days'.")

    print(f"Training set ends on {train_cutoff}, test set has {len(test_df)} rows.")

    train_df.rename(columns={date_col: 'ds', value_col: 'y'}, inplace=True)
    
    # Prophet model
    from prophet import Prophet
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(train_df[['ds', 'y']])

    last_test_date = test_df[date_col].max()  # This is a Timestamp

    # Now we can subtract safely because train_cutoff is also a Timestamp
    horizon = (last_test_date - train_cutoff).days
    
    future = model.make_future_dataframe(periods=horizon, freq='D')  
    forecast = model.predict(future)
    
    forecast_df = forecast[['ds', 'yhat']].copy()
    test_df = test_df.rename(columns={date_col: 'ds', value_col: 'actual'})
    
    merged = pd.merge(test_df, forecast_df, on='ds', how='left')
    merged = merged.dropna(subset=['yhat'])

    from sklearn.metrics import mean_absolute_error, mean_squared_error
    y_true = merged['actual'].values
    y_pred = merged['yhat'].values
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    
    return mae, mse


if __name__ == "__main__":
    # Example usage:
    # Suppose we have a CSV "revenue_data.csv" with columns ds (date) and y (daily revenue).
    data = pd.read_csv("./output/revenue_forecast.csv")
    
    mae_val, mse_val = evaluate_forecast_performance(
        data,
        date_col='ds',
        value_col='yhat',
        train_cutoff='2024-01-01',  # or None to auto-split
        forecast_days=90
    )
    
    # The function already prints MAE and MSE, but you can also handle them as variables
    print(f"Final results: MAE={mae_val}, MSE={mse_val}")
