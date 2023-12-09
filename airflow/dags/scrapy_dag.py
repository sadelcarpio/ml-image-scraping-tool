import airflow
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
}

with airflow.DAG(
    "example_http_operator",
    default_args=default_args,
) as dag:
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