import json

import confluent_kafka
from scrapy.utils.project import get_project_settings


class KafkaProducer(confluent_kafka.Producer):
    def __init__(self, bootstrap_servers: str, client_id: str) -> None:
        self.gcs_folder_path = get_project_settings()["GCS_FOLDER_PATH"]
        super().__init__({'bootstrap.servers': bootstrap_servers, 'client.id': client_id, 'acks': 'all'})

    def produce_urls(self, topic: str, filenames: list, scraping_project: str, prefix: str):
        for filename in filenames:
            msg = {"url": f"{prefix}/{self.gcs_folder_path}/{filename}", "project": scraping_project}
            super().produce(topic=topic, value=bytes(json.dumps(msg).encode('utf-8')))
