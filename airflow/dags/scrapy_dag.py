import airflow
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
}


def check_status():
    import time
    import requests
    try:
        finished = []
        while not finished:
            response = requests.get('http://scrapyd:6800/listjobs.json', timeout=10)
            response.raise_for_status()
            finished = response.json()['finished']
            running = response.json()['running']
            print("Web scraping status:", running)
            time.sleep(30)
        print("Web scraping finished", finished)
    except requests.exceptions.RequestException as e:
        print("Error on HTTP request:", e)
        return


with airflow.DAG(
        "example_http_operator",
        default_args=default_args,
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
