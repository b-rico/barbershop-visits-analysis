"""
File Name: gen_visits_table.py
Author: Bert Rico
Created: 2024-12-27
Description:
    This script generates 5 years of visits data for 1000 clients, including visit dates, client IDs,
    first visit dates, and randomly generated revenue values.
    
    The generated CSV file is saved in the specified data directory.
Args:
    - data_dir (str): The directory where the output CSV file will be saved.
Output:
    - A CSV file named 'visits_table.csv' saved to the specified data directory.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def gen_visits_table(data_dir):
    """
    Generate 5 years of visits data for 1000 clients.
    Saves the visits_table.csv into data_dir.
    """

    START_DATE = datetime(2020, 1, 1)
    END_DATE = datetime.now()
    np.random.seed(42)  # For reproducibility
    
    adjusted_data = []
    unique_client_ids = range(1, 1001)

    for client_id in unique_client_ids:
        category = np.random.choice(['Highly Loyal', 'Loyal', 'Low Loyalty', 'At Risk'], 
                                    p=[0.1, 0.4, 0.3, 0.2])
        
        if category == 'Highly Loyal':
            yearly_visits = np.random.randint(15, 20)
        elif category == 'Loyal':
            yearly_visits = np.random.randint(8, 15)
        elif category == 'Low Loyalty':
            yearly_visits = np.random.randint(4, 8)
        else:  
            yearly_visits = np.random.randint(1, 4)

        for year in range(2020, 2025):
            visits_this_year = int(yearly_visits * np.random.uniform(0.8, 1.2))
            months = np.random.choice(
                range(1, 13),
                size=visits_this_year,
                replace=True,
                p=[0.05, 0.08, 0.08, 0.10, 0.12, 0.12, 0.12, 0.10, 0.08, 0.08, 0.05, 0.02]
            )
            for month in months:
                day = np.random.randint(1, 28)  # keep it simple
                visit_date = datetime(year, month, day)
                adjusted_data.append({'id': client_id, 'date': visit_date})
    
    adjusted_data = pd.DataFrame(adjusted_data)
    adjusted_data['date'] = adjusted_data['date'].dt.strftime('%Y-%m-%d')
    adjusted_data['first_visit'] = adjusted_data.groupby('id')['date'].transform('min')
    adjusted_data['revenue'] = np.random.choice(
        [15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
        size=len(adjusted_data)
    )

    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, 'visits_table.csv')
    adjusted_data.to_csv(output_path, index=False)

    print(f"Visits table CSV saved to: {output_path}")

if __name__ == "__main__":
    gen_visits_table("./data")
