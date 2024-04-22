import os

from airflow.decorators import task
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from sqlalchemy import create_engine

IMAGES_TO_PROCESS = 1


def count_labeled_unprocessed_urls(project_name):
    engine = create_engine(
        f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@{os.environ.get('INSTANCE_NAME')}/{os.environ.get('POSTGRES_DB')}")
    with engine.connect() as connection:
        result = connection.execute(f"SELECT COUNT(*) FROM labels_for_processing WHERE project='{project_name}'")
        row_count = result.fetchone()[0]
    return row_count >= IMAGES_TO_PROCESS


def load_to_gcs():
    """
    Beam Docker operation to load the table of processed urls to a csv file on cloud storage
    :return:
    """
    return DockerOperator(
        task_id="load_to_gcs",
        image="beam-upload-csv",
        container_name="gcs_csv_load",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        command="--project=test-project-full",
        network_mode="mlist_default",
        environment={
            "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
            "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
            "INSTANCE_NAME": os.environ.get("INSTANCE_NAME")
        },
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False,
        mounts=[
            Mount(source=f"{os.getenv('PIPELINES_DIR')}/upload_csv_labels",
                  target="/src/upload_csv_labels", type="bind")
        ]
    )


@task()
def convert_to_tfrecord():

    """
    Beam Docker Operator to optionally convert your csv file to a TFRecord format.
    :return:
    """
    return DockerOperator(
        task_id="convert_to_tfrecord",
        image="hello-world",
        container_name="tfrecord",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False
    )
