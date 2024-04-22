from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import ShortCircuitOperator

from tasks.common import notify_owner
from tasks.etl_tasks import count_labeled_unprocessed_urls, convert_to_tfrecord, load_to_gcs, should_convert_tfrecord
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
            python_callable=count_labeled_unprocessed_urls,
            op_args=[dag_params.project]
        )

        tfrecord = should_convert_tfrecord()
        notify = notify_owner(dag_params)

        reached_target_labels >> load_to_gcs(dag_params.project) >> tfrecord
        tfrecord >> notify
        tfrecord >> convert_to_tfrecord() >> notify


    beam_etl_dag()
