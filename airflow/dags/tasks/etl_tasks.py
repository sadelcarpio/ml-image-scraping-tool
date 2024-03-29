from airflow.decorators import task

IMAGES_TO_PROCESS = 100


def count_labeled_unprocessed_urls():
    labeled_unprocessed_urls = 100
    return labeled_unprocessed_urls >= IMAGES_TO_PROCESS


@task()
def process_labeled_urls():
    print("We have reached the number of URLs. Processing ...")
