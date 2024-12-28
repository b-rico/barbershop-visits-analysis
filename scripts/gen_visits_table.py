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
    Generate 5 years of visits data for 1000 clients, allowing new clients
    to appear in later years (growth).

    Saves 'visits_table.csv' into data_dir.
    """
    np.random.seed(42)  
    start_years_distribution = (
        [2020] * 300 +
        [2021] * 200 +
        [2022] * 200 +
        [2023] * 200 +
        [2024] * 100
    )
    np.random.shuffle(start_years_distribution)
    
    unique_client_ids = list(range(1, 1001))
    
    all_visits = []
    
    for i, client_id in enumerate(unique_client_ids):
        start_year = start_years_distribution[i]

        category = np.random.choice(
            ['Highly Loyal', 'Loyal', 'Low Loyalty', 'At Risk'],
            p=[0.1, 0.4, 0.3, 0.2]
        )
        
        if category == 'Highly Loyal':
            yearly_visits = np.random.randint(15, 20)
        elif category == 'Loyal':
            yearly_visits = np.random.randint(8, 15)
        elif category == 'Low Loyalty':
            yearly_visits = np.random.randint(4, 8)
        else:  # 'At Risk'
            yearly_visits = np.random.randint(1, 4)

        for year in range(start_year, 2025): 
            visits_this_year = int(yearly_visits * np.random.uniform(0.8, 1.2))

            months = np.random.choice(
                range(1, 13),
                size=visits_this_year,
                replace=True,
                p=[0.05, 0.08, 0.08, 0.10, 0.12, 0.12, 0.12, 0.10, 0.08, 0.08, 0.05, 0.02]
            )
            for month in months:
                day = np.random.randint(1, 28) 
                visit_date = datetime(year, month, day)
                
                all_visits.append({
                    'id': client_id,
                    'date': visit_date
                })

    visits_df = pd.DataFrame(all_visits)
    
    if visits_df.empty:
        print("No visits generated. Check your distribution or category logic.")
        return

    visits_df['date'] = visits_df['date'].dt.strftime('%Y-%m-%d')

    visits_df['first_visit'] = visits_df.groupby('id')['date'].transform('min')

    visits_df['revenue'] = np.random.choice(
        [15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
        size=len(visits_df)
    )

    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, 'visits_table.csv')
    visits_df.to_csv(output_path, index=False)

    print(f"Visits table CSV saved to: {output_path}")

if __name__ == "__main__":
    gen_visits_table("./data")
