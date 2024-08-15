import pandas as pd

def client_visit_frequency_analysis(data, output_dir):
    data['visit_gap'] = data.groupby('id')['date'].diff().dt.days
    avg_time_between_visits = data.groupby('id')['visit_gap'].mean().reset_index()
    avg_time_between_visits.to_csv(f"{output_dir}/avg_time_between_visits.csv", index=False)
    print("Client Visit Frequency Analysis complete: avg_time_between_visits.csv generated.")
