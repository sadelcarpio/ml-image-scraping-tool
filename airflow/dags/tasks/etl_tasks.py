import os

from airflow.decorators import task
from sqlalchemy import create_engine

IMAGES_TO_PROCESS = 100


def count_labeled_unprocessed_urls():
    engine = create_engine(
        f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@{os.environ.get('INSTANCE_NAME')}/{os.environ.get('POSTGRES_DB')}")
    with engine.connect() as connection:
        result = connection.execute("SELECT COUNT(*) FROM labels_for_processing")
        row_count = result.fetchone()[0]
    return row_count >= 1


@task()
def process_labeled_urls():
    print("We have reached the number of URLs. Processing ...")
