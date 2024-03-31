import os

from airflow.decorators import task
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


@task()
def load_to_gcs():
    print("This should be a BeamOperator that takes the function / procedure / view for the project"
          " and uploads its content as a csv file to GCS.")


@task()
def convert_to_tfrecord():
    print("This optional branch should convert the csv files to tfrecord (sample already done but need some"
          " modification)")
