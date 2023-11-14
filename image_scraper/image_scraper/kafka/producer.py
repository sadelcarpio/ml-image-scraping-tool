import confluent_kafka
from scrapy.utils.project import get_project_settings


class KafkaProducer(confluent_kafka.Producer):
    def __init__(self, bootstrap_servers: str, client_id: str) -> None:
        self.gcs_folder_path = get_project_settings()["GCS_FOLDER_PATH"]
        super().__init__({'bootstrap.servers': bootstrap_servers, 'client.id': client_id})

    def produce_urls(self, topic: str, filenames: list, prefix: str):
        for filename in filenames:
            url = f"{prefix}/{self.gcs_folder_path}/{filename}"
            super().produce(topic=topic, value=bytes(url.encode('utf-8')))
