import pandas as pd

def client_retention_loyalty_metrics(data, output_dir):
    """
    This function calculates client retention and loyalty metrics based on their visit data.
    
    - Retention is defined as clients who have visited more than once.
    - The function will also calculate the total number of visits for each client.

    Args:
    - data (DataFrame): The DataFrame containing client visit data with at least 'id' and 'date' columns.
    - output_dir (str): The directory where the output CSV file will be saved.

    Output:
    - A CSV file named 'client_retention_loyalty.csv' saved to the specified output directory.
    """
    # Calculate the total number of visits for each client
    retention = data.groupby('id')['date'].count().reset_index(name='visit_count')
    
    # Determine whether the client is retained (i.e., has visited more than once)
    retention['retained'] = retention['visit_count'] > 1
    
    # Add loyalty categorization
    conditions = [
        (retention['visit_count'] >= 10),
        (retention['visit_count'] >= 5) & (retention['visit_count'] < 10),
        (retention['visit_count'] < 5)
    ]
    choices = ['Highly Loyal', 'Loyal', 'Low Loyalty']
    retention['loyalty'] = pd.cut(retention['visit_count'], bins=[0, 4, 9, float('inf')], labels=choices, include_lowest=True)
    
    # Save the results
    retention.to_csv(f"{output_dir}/client_retention_loyalty.csv", index=False)
    print("Client Retention and Loyalty Metrics complete: client_retention_loyalty.csv generated.")
