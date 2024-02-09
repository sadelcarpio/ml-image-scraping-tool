from datetime import datetime

import requests
from airflow.decorators import dag, task

from utils.dag_data import dags_metadata

for dag_params in dags_metadata:

    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "email_on_failure": True,
        "email": dag_params.notify
    }


    @dag(
        dag_params.project + "_scraping",
        default_args=default_args,
        start_date=datetime(2023, 12, 1),
        schedule="@daily",
        catchup=False,
        tags=["image_scraping"]
    )
    def image_scraping_dag():

        @task()
        def schedule_spider():
            response_status = requests.post("http://scrapyd:6800/schedule.json",
                                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                                            data={"project": "image_scraper",
                                                  "spider": "google_images_spider",
                                                  "scraping_project": dag_params.project,
                                                  "start_urls": dag_params.keywords})
            return response_status.json()

        @task()
        def wait():
            import time
            time.sleep(30)

        @task()
        def check_scraping_status(*, ti=None):
            import time
            import requests
            import logging

            logger = logging.getLogger(__name__)
            response_status = ti.xcom_pull(task_ids="schedule_spider")
            job_id = response_status["jobid"]
            try:
                job_finished_status = []
                while not job_finished_status:
                    response = requests.get('http://scrapyd:6800/listjobs.json', timeout=10)
                    response.raise_for_status()
                    finished = response.json()['finished']
                    running = response.json()['running']
                    job_finished_status = list(filter(lambda job: job["id"] == job_id, finished))
                    if job_finished_status:
                        logger.info(f"Web scraping finished: {job_finished_status[0]}")
                        return
                    job_running_status = list(filter(lambda job: job["id"] == job_id, running))
                    logger.info(f"Web scraping status: {job_running_status[0]}")
                    time.sleep(30)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error on HTTP request: {e}")
                return

        @task()
        def notify_owner():
            from airflow.utils.email import send_email
            send_email(to=dag_params.notify,
                       subject=f"Dag for {dag_params.project} completed",
                       html_content=f"Dag finished successfully!")

        schedule_spider() >> wait() >> check_scraping_status() >> notify_owner()


    image_scraping_dag()
