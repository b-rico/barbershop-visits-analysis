# Barbershop Client Visit Analysis

This project is designed to help you analyze and gain insights from barbershop client visit data. By running the provided Python scripts, you'll be able to understand client behavior, identify patterns, and make data-driven decisions to improve client retention and operational efficiency.

## Data Source

The data used in this project was retrieved from Kaggle (https://www.kaggle.com/datasets/fredericobaker/barber-shop-frequency-data/data). It contains information about the frequency of client visits to a barbershop, including the client ID and the date of each visit.

## Project Structure

Here's how the project is organized:

main.py: This is the main script that runs all the analyses in sequence and saves the results in the ./output folder.

scripts/: This folder contains individual scripts for each type of analysis:

-client_visit_frequency_analysis.py: Analyzes the average time between visits for each client.
-client_retention_loyalty_metrics.py: Calculates client retention rates and segments clients based on their loyalty.
-trend_analysis.py: Identifies trends in client visits over time.
-predictive_analytics.py: Predicts the next visit date for each client based on their visit history.
-client_lifetime_value.py: Estimates the lifetime value of each client based on their visit frequency.
-churn_analysis.py: Analyzes churn by identifying clients who haven't visited recently.
-loyalty_segmentation.py: Segments clients into different loyalty categories based on visit frequency and recency.
-visit_patterns.py: Analyzes visit patterns by day of the week and month.

## Installation

- Step 1: Clone the Repository
To get started, you need to clone this repository to your local machine. You can do this by running the following command in your terminal or command prompt:

```bash
git clone https://github.com/yourusername/barbershop-client-visit-analysis.git
cd barbershop-client-visit-analysis
```

- Step 2: Install the Required Python Packages
Next, you'll need to install the necessary Python packages. These packages are listed in the requirements.txt file. To install them, run:

```bash
pip install -r requirements.txt
```

- Step 3: Prepare Your Data
Place your client visit data (CSV file) in the root directory of the project. The file should contain at least the following columns:

id: The unique identifier for each client.
date: The date of each visit.

- Step 4: Run the Analysis

Finally, you can run the analysis by executing the main.py script:

```bash
python main.py
```

The results of each analysis will be saved in the ./output directory in CSV format.

## Recommended Visualizations and Why

Once you have the output data, you can visualize it using tools like Looker Studio, Excel, or any other data visualization software. Here are some recommendations for each type of analysis:

### 1. Average Time Between Visits (avg_time_between_visits.csv)

Recommended Visualization: Box Plot or Histogram

Why: These charts help you understand the distribution of average time between visits. A box plot will show you the spread and identify outliers, while a histogram will show you the frequency of different intervals.

### 2. Client Retention and Loyalty Metrics (client_retention_loyalty.csv)

Recommended Visualization: Stacked Bar Chart or Pie Chart

Why: A stacked bar chart can display the proportion of clients in each loyalty segment, giving you a quick overview of your customer base. A pie chart can be used to show the percentage of retained versus non-retained clients.

### 3. Monthly Visits Trend (monthly_visits_trend.csv)

Recommended Visualization: Line Chart or Area Chart

Why: A line or area chart is perfect for visualizing trends over time, such as identifying busy seasons or spotting any upward or downward trends in visits.

### 4. Predicted Next Visits (predicted_next_visits.csv)

Recommended Visualization: Calendar Heatmap or Scatter Plot

Why: A calendar heatmap can visually show the predicted busy days, helping you prepare for peak times. A scatter plot can show the relationship between the last visit and the predicted next visit.

### 5. Client Lifetime Value (client_lifetime_value.csv)

Recommended Visualization: Bar Chart or Scatter Plot

Why: A bar chart can help rank clients by their lifetime value, making it easy to see who your most valuable clients are. A scatter plot can show how visit frequency correlates with lifetime value.

### 6. Churn Analysis (churn_analysis.csv)

Recommended Visualization: Pie Chart or Donut Chart

Why: These charts can clearly show the proportion of clients who have churned versus those who are still active, making it easy to gauge overall client retention.

### 7. Loyalty Segmentation (loyalty_segmentation.csv)

Recommended Visualization: Treemap or Stacked Bar Chart

Why: A treemap can provide a hierarchical view of client segments based on loyalty, while a stacked bar chart can show the distribution across different segments.

### 8. Visit Patterns by Day of the Week and Month (day_of_week_patterns.csv, month_patterns.csv)

Recommended Visualization: Heatmap or Bar Chart

Why: A heatmap is great for identifying patterns in client visits across days and months. A bar chart can separately show which days of the week and which months are most popular.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions that improve the analysis scripts, add new features, or enhance documentation are welcome!

License
This project is licensed under the MIT License. You can use, modify, and distribute this code as you see fit.