from datetime import datetime

from airflow.decorators import dag
from airflow.operators.python import ShortCircuitOperator

from tasks.common import notify_owner
from tasks.etl_tasks import process_labeled_urls, count_labeled_unprocessed_urls
from utils.dag_data import get_dag_metadata

for dag_params in get_dag_metadata():

    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "email_on_failure": True,
        "email": dag_params.notify
    }


    @dag(
        dag_params.project.replace(" ", "-").lower() + "_etl",
        default_args=default_args,
        start_date=datetime(2023, 12, 1),
        schedule="@daily",
        catchup=False,
        tags=["beam_etl"]
    )
    def beam_etl_dag():
        reached_target_labels = ShortCircuitOperator(
            task_id="check_target_labels_reached",
            python_callable=count_labeled_unprocessed_urls
        )
        reached_target_labels >> process_labeled_urls() >> notify_owner(dag_params)

    beam_etl_dag()
