# Barbershop Client Visit Analysis

This project provides a set of Python scripts to analyze and derive insights from barbershop client visit data. The scripts focus on understanding client behavior, visit patterns, and loyalty, which can help in making data-driven decisions for improving client retention and operational efficiency.

## Project Structure

main.py: The main script that runs all analyses sequentially and saves the results to the ./output folder.

## scripts/:

client_visit_frequency_analysis.py: Analyzes the average time between visits for each client.
client_retention_loyalty_metrics.py: Calculates client retention rates and segments clients based on loyalty.
trend_analysis.py: Identifies trends in client visits over time.
predictive_analytics.py: Predicts the next visit date for each client based on historical data.
client_lifetime_value.py: Estimates the lifetime value of clients based on visit frequency.
churn_analysis.py: Analyzes churn by identifying clients who haven't visited recently.
loyalty_segmentation.py: Segments clients into loyalty categories based on visit frequency and recency.
visit_patterns.py: Analyzes visit patterns by day of the week and month.

## Installation

To run the analyses, follow these steps:

Clone the Repository:

    ```bash
    git clone https://github.com/yourusername/barbershop-client-visit-analysis.git
    cd barbershop-client-visit-analysis
    ```

## Install Dependencies:

Ensure you have Python installed. You can install the necessary Python packages using:

    ```bash
    pip install -r requirements.txt
    ```

## Place Your Data:

Place your client visit data (CSV file) in the root directory of the project.

Data used for this project came from kaggle (https://www.kaggle.com/datasets/fredericobaker/barber-shop-frequency-data/data)

## Usage

### Running the Analysis:

To execute all the scripts and generate the output, run:

    ```bash
    Copy code
    python main.py
    ```
### Results:

The results of each analysis will be saved in the ./output directory in CSV format. The following files will be generated:

avg_time_between_visits.csv: Average time between visits for each client.
client_retention_loyalty.csv: Client retention and loyalty metrics.
monthly_visits_trend.csv: Trend analysis of client visits over time.
predicted_next_visits.csv: Predicted next visit dates for each client.
client_lifetime_value.csv: Estimated lifetime value for each client.
churn_analysis.csv: Churn analysis identifying clients at risk.
loyalty_segmentation.csv: Loyalty segmentation of clients.
day_of_week_patterns.csv & month_patterns.csv: Visit patterns by day of the week and month.

## Customization

Modifying Scripts: If you need to modify the logic of any analysis, you can edit the corresponding script in the scripts/ directory.

## Changing Parameters: You can adjust thresholds or parameters (e.g., churn threshold) directly in the respective scripts.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.