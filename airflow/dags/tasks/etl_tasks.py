import os

from airflow.decorators import task
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from sqlalchemy import create_engine

IMAGES_TO_PROCESS = 1


@task.branch(task_id="should_convert_to_tfrecord")
def should_convert_tfrecord():
    return "notify_owner"  # branch depending on task_id


def count_labeled_unprocessed_urls(project_name: str):
    engine = create_engine(
        f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@{os.environ.get('INSTANCE_NAME')}/{os.environ.get('POSTGRES_DB')}")
    with engine.connect() as connection:
        result = connection.execute(f"SELECT COUNT(*) FROM labels_for_processing WHERE project='{project_name}'")
        row_count = result.fetchone()[0]
    return row_count >= IMAGES_TO_PROCESS


@task
def update_last_processed(project_name: str):
    import requests
    from datetime import datetime
    response = requests.patch(f"http://update-last-processed:5000/{project_name}",
                              json={"date_str": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")})
    response.raise_for_status()


def load_to_gcs(project_name: str, last_processed: str):
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
        command=f'--project="{project_name}" --last_processed="{last_processed}"',
        network_mode="mlist_default",
        environment={
            "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
            "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
            "INSTANCE_NAME": os.environ.get("INSTANCE_NAME"),
            "LABELS_BUCKET": os.environ.get("LABELS_BUCKET")
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
