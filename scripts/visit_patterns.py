import pandas as pd

def visit_patterns(data, output_dir):
    """
    This function analyzes the visit patterns of clients by day of the week and month.
    It helps identify trends in when clients are most likely to visit.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'date' column.
    - output_dir (str): The directory where the output CSV files will be saved.

    Output:
    - Two CSV files named 'day_of_week_patterns.csv' and 'month_patterns.csv' saved to the specified output directory.
    """
    # Ensure the date column is in datetime format
    data['date'] = pd.to_datetime(data['date'])
    
    # Extract the day of the week and month from the date
    data['day_of_week'] = data['date'].dt.day_name()
    data['month'] = data['date'].dt.month_name()
    
    # Count the number of visits per day of the week
    day_of_week_patterns = data['day_of_week'].value_counts().reset_index(name='visit_count')
    day_of_week_patterns.columns = ['day_of_week', 'visit_count']
    
    # Count the number of visits per month
    month_patterns = data['month'].value_counts().reset_index(name='visit_count')
    month_patterns.columns = ['month', 'visit_count']
    
    # Save the results
    day_of_week_patterns.to_csv(f"{output_dir}/day_of_week_patterns.csv", index=False)
    month_patterns.to_csv(f"{output_dir}/month_patterns.csv", index=False)
    print("Visit Patterns Analysis complete: day_of_week_patterns.csv and month_patterns.csv generated.")
