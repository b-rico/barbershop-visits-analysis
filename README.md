# Barbershop Client Visit Analysis
This project provides a comprehensive suite of analytics and insights for barbershop client visit data. By running the Python scripts provided, you can analyze client behavior, forecast visits and revenue, identify trends, and make data-driven decisions to improve client retention and operational efficiency.

## Data Source
This project generates mock data if no dataset is found (see Data Generation).

## Project Structure

```bash
Project Git Tree
    ├─ main.py
    ├─ data/
    ├─ output/
    ├─ scripts/
    │   ├─ gen_visits_table.py
    │   ├─ gen_clients_table.py
    │   ├─ client_visit_frequency_analysis.py
    │   ├─ client_retention_loyalty_metrics.py
    │   ├─ trend_analysis.py
    │   ├─ predictive_analytics.py
    │   ├─ predictive_analytics_survival.py
    │   ├─ client_lifetime_value.py
    │   ├─ churn_analysis.py
    │   ├─ loyalty_segmentation.py
    │   ├─ visit_patterns.py
    │   └─ time_series_forecast.py
    └─ tests/
        ├─ test_client_visit_frequency_analysis.py
        ├─ test_predictive_analytics_survival.py
        ├─ test_time_series_forecast.py
        └─ ...
```
- main.py: Orchestrates the entire pipeline. Checks if visits_table.csv exists, and if not, triggers data generation. Runs all analysis scripts in sequence and saves the results to ./output.

- data/: Contains the input CSV files (e.g., visits_table.csv, clients_table.csv). If these files are missing, the generation scripts will create them.

- output/: Stores the output CSV results from each analysis (e.g., avg_time_between_visits.csv, predicted_next_visits_survival.csv, etc.).

- scripts/: Contains all individual Python scripts for data generation and analytics.

## Data Generation:

- gen_visits_table.py: Generates a mock visits_table.csv with random visits, dates, and revenue if the file does not already exist.
- gen_clients_table.py: Generates a mock clients_table.csv with random client demographic data.

## Analysis Scripts:

- client_visit_frequency_analysis.py
    Analyzes average time between visits for each client.
- client_retention_loyalty_metrics.py
    Calculates client retention metrics and loyalty segments.
- trend_analysis.py
    Identifies monthly or daily trends in client visits.
- predictive_analytics.py
    Uses a simple average gap approach to predict the next visit date for each client.
- predictive_analytics_survival.py
    Uses survival analysis (Cox Proportional Hazards) to predict each client’s next visit date more robustly.
- client_lifetime_value.py
    Updated to use the revenue field for each visit, calculating total lifetime revenue per client.
- churn_analysis.py
    Identifies clients who have not visited within a specified threshold (e.g., 180 days).
- loyalty_segmentation.py
    Segments clients into loyalty categories based on frequency and recency of visits.
- visit_patterns.py
    Analyzes visits by day of the week and month, producing patterns in user traffic.
- time_series_forecast.py
    New script that uses Meta/Facebook Prophet to forecast daily visits and daily revenue for a given future horizon.
- tests/: Contains test scripts (using either unittest or pytest) for validating the logic of each analysis script. For example, test_predictive_analytics_survival.py tests the survival analysis pipeline end to end.

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/barbershop-client-visit-analysis.git
cd barbershop-client-visit-analysis
Create and Activate a Virtual Environment (Recommended)
```

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
Install Required Python Packages
```

```bash
Copy code
pip install -r requirements.txt
(Optional) Provide Your Own Data
```

If you have your own visits data, place it at ./data/visits_table.csv (and optionally a clients_table.csv).
Otherwise, if visits_table.csv is not found, the project’s data generation scripts (gen_visits_table.py, gen_clients_table.py) will automatically run to create mock data.

## Run the Analysis

```bash
python main.py
The scripts will:
```

1.  Generate data if missing.
2. Perform each analysis step in sequence.
3. Write outputs (CSV files) into ./output.

### Data Generation
    If visits_table.csv does not exist in the ./data folder, main.py will call:

    - gen_visits_table.py: Creates a random set of visits over a 5-year window, including dates and revenue amounts.
    - gen_clients_table.py: Creates a mock client list (ID, name, address, demographics, etc.).

    These files will appear under ./data/:

    - visits_table.csv
    - clients_table.csv

## Scripts Overview

- client_visit_frequency_analysis.py
    Generates avg_time_between_visits.csv, which shows the average gap between visits per client.

- client_retention_loyalty_metrics.py
    Produces client_retention_loyalty.csv, showing retention rates and loyalty tiers.

- trend_analysis.py
    Outputs monthly_visits_trend.csv (or a similar file) with aggregated visits by month (or week).

- predictive_analytics.py
    Outputs predicted_next_visits.csv using a simple average-day-gap method.

- predictive_analytics_survival.py
    Creates a more robust next-visit forecast using survival analysis.
    Writes predicted_next_visits_survival.csv to ./output.

- client_lifetime_value.py
    Sums each client’s actual revenue across all visits to compute total lifetime value.
    Saves client_lifetime_value.csv.

- churn_analysis.py
    Creates churn_analysis.csv by identifying clients who haven’t visited in a specified threshold (e.g., 180 days).

- loyalty_segmentation.py
    Outputs loyalty_segmentation.csv, segmenting clients into categories based on loyalty behaviors.

- visit_patterns.py
    Creates day_of_week_patterns.csv and month_patterns.csv, analyzing which days/months see the highest visits.

- time_series_forecast.py
    New script that uses Prophet to forecast daily visits and daily revenue.
    Generates visit_forecast.csv and revenue_forecast.csv for the specified forecast horizon (e.g. 30 days).

## Running Unit Tests

This project uses Python’s built-in unittest (and sometimes pytest). Test scripts live in ./tests.

To run them (with unittest):

```bash
python -m unittest discover tests
```
1. test_client_visit_frequency_analysis.py
    Purpose: Verifies that the average time between visits is calculated correctly.
    Key Checks:
    File output: Ensures an output CSV (e.g., avg_time_between_visits.csv) is created.
    Columns: Checks that expected columns (like id, avg_days_between_visits) exist.
    Values: Optionally checks the numeric ranges or data types.
2. test_predictive_analytics.py (if present)
    Purpose: Tests the simple average-gap-based next visit prediction script.
    Key Checks:
    Computation: Ensures the function that calculates average day gap per client does not crash and yields numeric predictions.
    CSV Output: Verifies that predicted_next_visits.csv is generated with expected columns (id, last_visit_date, predicted_next_visit).
    Accuracy: Might compare actual vs. expected predictions in a controlled dataset.
3. test_predictive_analytics_survival.py
    Purpose: Validates the survival-analysis approach (Cox model) to predicting next visits.
    Key Checks:
    create_survival_dataset_from_df:
    Confirms the resulting DataFrame has the columns duration, event, and revenue_feature.
    Checks that duration is numeric and event is either 0 or 1.
    fit_cox_model:
    Ensures a Cox model is created without errors.
    predict_next_visit:
    Verifies that a single “most recent visit + feature” scenario returns either a valid timestamp or None.
    Ensures times passed to the survival function do not exceed the domain (or you handle it gracefully).
    predictive_analytics_survival_df:
    Runs the full pipeline end to end on a mock dataset.
    Checks for the output file predicted_next_visits_survival.csv.
    Asserts expected columns (id, last_visit_date, predicted_next_visit) are present.
4. test_time_series_forecast.py
    Purpose: Tests the Prophet-based forecasting script for daily visits and revenue.
    Key Checks:
    Mock Data Generation: Creates artificial daily data for a small date range with random visits/revenue.
    Forecast Execution: Ensures the script runs time_series_forecast without errors.
    Files Created: Checks for visit_forecast.csv and revenue_forecast.csv.
    Column Presence: Confirms that typical Prophet output columns (ds, yhat, yhat_lower, yhat_upper) exist.
    Forecast Rows: Asserts that the forecast includes future dates beyond the historical data.
5. test_churn_analysis.py (if present)
    Purpose: Validates the script that identifies clients who have not visited within a certain threshold.
    Key Checks:
    Threshold Logic: Tests that the script correctly flags clients who surpass the churn threshold (e.g., 180 days since last visit).
    Output File: Verifies churn_analysis.csv is created and has columns such as id, last_visit_date, is_churned.
    Edge Cases: Possibly tests a client exactly on the threshold or a client with no visits.
6. test_client_lifetime_value.py (if present)
    Purpose: Checks the updated LTV script that now sums revenue for each client.
    Key Checks:
    Revenue Summation: Ensures the function properly sums multiple visits’ revenues for each id.
    Output: Verifies the existence of client_lifetime_value.csv with columns like id and lifetime_value.
    Basic Data Integrity: Possibly checks for negative or zero revenue edge cases.
7. test_gen_visits_table.py and test_gen_clients_table.py (if present)
    Purpose: Tests the data generation scripts to ensure they produce valid CSV files with the expected columns.
    Key Checks:
    File Creation: Asserts that visits_table.csv or clients_table.csv actually appear in ./data.
    Column Presence: Checks required fields (e.g., id, date, revenue in visits; id, first_name, etc. in clients).
    Row Counts: Might confirm you generated the expected approximate number of rows (e.g., 1000 clients x multiple visits).

## Visualization Recommendations

After running the analyses, you’ll have several CSV files in ./output. Below are suggestions for how to visualize some of these outputs:

### Average Time Between Visits (avg_time_between_visits.csv)
    Histogram or Box Plot to understand distribution of intervals.

### Client Retention and Loyalty (client_retention_loyalty.csv)
    Stacked Bar or Pie Chart to show loyalty segments or retention rates.

### Monthly Visits Trend (monthly_visits_trend.csv)
    Line or Area Chart to observe seasonal trends.

### Predicted Next Visits - Simple (predicted_next_visits.csv)
    Calendar Heatmap or Scatter Plot to see upcoming busy days.

### Predicted Next Visits - Survival Analysis (predicted_next_visits_survival.csv)
    Similar visualization as above; consider comparing both methods if desired.

### Client Lifetime Value (client_lifetime_value.csv)
    Bar Chart ranking clients by LTV, or Scatter Plot comparing visits vs. total revenue.

### Churn Analysis (churn_analysis.csv)
    Pie/Donut Chart to highlight churned vs. active clients.

### Loyalty Segmentation (loyalty_segmentation.csv)
    Treemap or Stacked Bar to display distribution of loyalty segments.

### Day/Month Visit Patterns (day_of_week_patterns.csv, month_patterns.csv)
    Heatmap or Bar Chart to pinpoint popular days/months.

### Forecast Output (visit_forecast.csv, revenue_forecast.csv)
    Line Chart with confidence intervals to show how visits/revenue may evolve over the forecast horizon.

## Contributing
Have improvements or new ideas?

Fork the repository.
Create a feature branch for your changes.
Submit a pull request describing your updates.
We welcome contributions that extend the analytics, add new tests, or improve documentation.

## License
This project is available under the MIT License. You can freely use, modify, and distribute this code for both personal and commercial purposes. See the [LICENSE](LICENSE) file for details.

Enjoy analyzing your barbershop client data! If you have any questions or issues, please open an issue or reach out with a pull request.