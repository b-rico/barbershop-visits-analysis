import pandas as pd

def client_lifetime_value(data, output_dir, avg_revenue_per_visit=50):
    """
    This function estimates the Client Lifetime Value (CLV) based on the number of visits and 
    an assumed average revenue per visit.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.
    - avg_revenue_per_visit (float): The assumed average revenue generated per visit (default is $50).

    Output:
    - A CSV file named 'client_lifetime_value.csv' saved to the specified output directory.
    """
    # Calculate the total number of visits for each client
    visit_counts = data.groupby('id')['date'].count().reset_index(name='total_visits')
    
    # Estimate the Client Lifetime Value (CLV)
    visit_counts['lifetime_value'] = visit_counts['total_visits'] * avg_revenue_per_visit
    
    # Save the results
    visit_counts.to_csv(f"{output_dir}/client_lifetime_value.csv", index=False)
    print("Client Lifetime Value Analysis complete: client_lifetime_value.csv generated.")
