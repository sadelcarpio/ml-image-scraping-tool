from datetime import datetime

import airflow
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from job_parameters.dag_data import METADATA

from utils.scrapyd_request import check_status

default_args = {
    "owner": "airflow",
    "depends_on_past": False
}

domain = "https://www.google.com/search?q="

for dag_params in METADATA:
    with airflow.DAG(
            dag_params["name"],
            default_args=default_args,
            start_date=datetime(2023, 12, 1),
            schedule="@daily",
            catchup=False
    ) as dag:
        schedule_spider_task = SimpleHttpOperator(
            task_id="schedule-spider",
            http_conn_id="scrapyd_http_endpoint",
            endpoint='schedule.json',
            data=f"project=image_scraper&spider=google_images_spider&start_url={domain}{dag_params['tag']}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method='POST',
            do_xcom_push=True,
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
            dag=dag,
        )

    schedule_spider_task >> wait_task >> check_status_task
