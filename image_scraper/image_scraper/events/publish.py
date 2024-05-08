import json
import os

import confluent_kafka
from google.cloud import pubsub
from scrapy.utils.project import get_project_settings


class MessagePublisher:
    def send_urls(self, topic: str, filenames: list, scraping_project: str, prefix: str):
        pass


class KafkaProducer(MessagePublisher):
    def __init__(self, bootstrap_servers: str, client_id: str) -> None:
        self.client = confluent_kafka.Producer({'bootstrap.servers': bootstrap_servers,
                                                'client.id': client_id,
                                                'acks': 'all'})
        self.gcs_folder_path = get_project_settings()["GCS_FOLDER_PATH"]

    def send_urls(self, topic: str, filenames: list, scraping_project: str, prefix: str):
        for filename in filenames:
            msg = {"url": f"{prefix}/{self.gcs_folder_path}/{filename}", "project": scraping_project}
            self.client.produce(topic=topic, value=bytes(json.dumps(msg).encode('utf-8')))


class PubSubPublisher(MessagePublisher):
    def __init__(self, **kwargs: any):
        self.client = pubsub.PublisherClient()
        self.gcs_folder_path = get_project_settings()["GCS_FOLDER_PATH"]
        self.project_id = get_project_settings()["GCS_PROJECT_ID"]
        super().__init__(**kwargs)

    def send_urls(self, topic: str, filenames: str, scraping_project: str, prefix: str):
        for filename in filenames:
            msg = {"url": f"{prefix}/{self.gcs_folder_path}/{filename}", "project": scraping_project}
            self.client.publish(topic=self.client.topic_path(os.environ['PROJECT_ID'], topic),
                                data=bytes(json.dumps(msg).encode('utf-8')))
            # future.result()


class MessagePublisherCreator:
    def create_publisher(self, **kwargs) -> MessagePublisher:
        raise NotImplementedError()


class KafkaProducerCreator(MessagePublisherCreator):
    def create_publisher(self, bootstrap_servers: str, client_id: str) -> MessagePublisher:
        return KafkaProducer(bootstrap_servers=bootstrap_servers, client_id=client_id)


class PubSubPublisherCreator(MessagePublisherCreator):
    def create_publisher(self, **kwargs) -> MessagePublisher:
        return PubSubPublisher(**kwargs)
