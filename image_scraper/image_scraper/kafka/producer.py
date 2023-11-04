import confluent_kafka
from image_scraper.settings import GCS_FOLDER_PATH


class KafkaProducer(confluent_kafka.Producer):
    def __init__(self, bootstrap_servers: str, client_id: str) -> None:
        super().__init__({'bootstrap.servers': bootstrap_servers, 'client.id': client_id})

    def produce_urls(self, topic: str, filenames: list, prefix: str):
        for filename in filenames:
            url = f"{prefix}/{GCS_FOLDER_PATH}/{filename}"
            super().produce(topic=topic, value=bytes(url.encode('utf-8')))
