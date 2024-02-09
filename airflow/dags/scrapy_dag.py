from datetime import datetime

from airflow.decorators import dag

from dags.tasks import schedule_spider, wait, check_scraping_status, notify_owner
from utils.dag_data import get_dag_metadata

for dag_params in get_dag_metadata():

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

        schedule_spider(dag_params) >> wait() >> check_scraping_status() >> notify_owner(dag_params)


    image_scraping_dag()
