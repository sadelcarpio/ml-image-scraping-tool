from datetime import datetime

import airflow
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

from utils.scrapyd_request import check_status

default_args = {
    "owner": "airflow",
    "depends_on_past": False
}

with airflow.DAG(
        "example_http_operator",
        default_args=default_args,
        start_date=datetime(2023, 12, 1),
        schedule_interval="@daily",
        catchup=False
) as dag:
    task = SimpleHttpOperator(
        task_id="schedule-spider",
        http_conn_id="scrapyd_http_endpoint",
        endpoint='schedule.json',
        data="project=image_scraper&spider=google_images_spider&start_url=https://www.google.com/search?q=dogs+images",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method='POST',
        dag=dag,
    )

    wait_task = BashOperator(
        task_id="wait",
        bash_command="sleep 30",  # Espera 30 segundos, ajusta según sea necesario
        dag=dag,
    )

    check_status_task = PythonOperator(
        task_id='check_scraping_status',
        python_callable=check_status,
        provide_context=True,
        dag=dag,
    )

task >> wait_task >> check_status_task
