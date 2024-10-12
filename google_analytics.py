import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

load_dotenv(find_dotenv())

# Replace these variables with your actual database credentials
db_username = os.getenv('USERNAME')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')
db_port = os.getenv('PORT')
db_name = os.getenv('DATABASE')

def data_googleAnalitycs_report():
    """Get a report from the Google Analytics API."""
    client = BetaAnalyticsDataClient()

    property_id = os.getenv('PROPERTY_ID')
    start_date = os.getenv('START_DATE')

    # Define the proper Dimension and Metric objects
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date"),
            Dimension(name="city"),
            Dimension(name="country"),
            Dimension(name="deviceCategory"),
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
        ],
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="newUsers"),
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViews"),
            Metric(name="conversions"),
            Metric(name="totalRevenue"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date="today")],
    )
    response = client.run_report(request)

    # Create lists to store the data
    data = []
    header = [dim.name for dim in request.dimensions] + [metric.name for metric in request.metrics]

    # Complete the list of data
    for row in response.rows:
        row_data = [dim_value.value for dim_value in row.dimension_values] + [metric_value.value for metric_value in row.metric_values]
        data.append(row_data)
    
    # Create a DataFrame with the data
    df = pd.DataFrame(data, columns=header)

    # Configuration for the database connection (PostgreSQL)
    db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(db_url)

    # Save the DataFrame on table 'google_analytics_data'
    df.to_sql(name='google_analytics_data', con=engine, if_exists='replace', index=False)

    print("Data saved to 'google_analytics_data' table.")

if __name__ == "__main__":
    data_googleAnalitycs_report()
