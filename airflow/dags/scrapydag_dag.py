import json
import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

dag = DAG(
    "example_http_operator",
    start_date=days_ago(2),
    default_args={"owner": "airflow"},
)

task = SimpleHttpOperator(
    task_id="schedule-spider",
    http_conn_id = "scrapyd_http_endpoint",
    endpoint='schedule.json',
    data="project=image_scraper&spider=google_images_spider&start_url=https://www.google.com/search?q=dogs+images",   # Any data you want to post
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    method='POST',
    dag=dag,
)

task