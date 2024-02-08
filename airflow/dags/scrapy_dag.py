from datetime import datetime

import airflow
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from parameters.dag_data import dags_metadata

from utils.scrapyd_request import check_status

for dag_params in dags_metadata:

    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "email_on_failure": True,
        "email": dag_params.notify
    }

    with airflow.DAG(
            dag_params.project,
            default_args=default_args,
            start_date=datetime(2023, 12, 1),
            schedule="@daily",
            catchup=False
    ) as dag:
        schedule_spider_task = SimpleHttpOperator(
            task_id="schedule-spider",
            http_conn_id="scrapyd_http_endpoint",
            endpoint='schedule.json',
            data=f"project=image_scraper&spider=google_images_spider&scraping_project={dag_params.project}"
                 f"&start_urls={dag_params.keywords}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method='POST',
            do_xcom_push=True,
            dag=dag,
        )

        wait_task = BashOperator(
            task_id="wait",
            bash_command="sleep 30",
            dag=dag,
        )

        check_status_task = PythonOperator(
            task_id='check_scraping_status',
            python_callable=check_status,
            dag=dag,
        )

    schedule_spider_task >> wait_task >> check_status_task
