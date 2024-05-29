import confluent_kafka
import os
from google.cloud import pubsub


class MessageSubscriber:
    client = None
    topic = None

    def receive_url(self):
        pass


class KafkaConsumer(MessageSubscriber):
    def __init__(self, bootstrap_servers: str, group_id: str, topic: str) -> None:
        self.client = confluent_kafka.Consumer({'bootstrap.servers': bootstrap_servers,
                                                'group.id': group_id})
        self.topic = topic
        self.client.subscribe([self.topic])

    def receive_url(self):
        msg = self.client.poll(0.1)  # look into consumer.consume() for batch processing
        return msg.value().decode("utf-8") if msg else None


class PubSubSubscriber(MessageSubscriber):
    def __init__(self, subscription_id: str, topic: str = None):
        self.client = pubsub.SubscriberClient()
        self.subscription_path = self.client.subscription_path(os.environ["PROJECT_ID"], subscription_id)
        self.topic = topic
        if not topic:
            self.topic = subscription_id

    def receive_url(self):
        response = self.client.pull(
            request={
                "subscription": self.subscription_path,
                "max_messages": 1,
            }
        )
        if not response.received_messages:
            return
        for msg in response.received_messages:
            message_data = msg.message.data.decode("utf-8")
            return message_data


class MessageSubscriberCreator:
    def create_publisher(self, **kwargs) -> MessageSubscriber:
        raise NotImplementedError()


class KafkaProducerCreator(MessageSubscriberCreator):
    def create_publisher(self, bootstrap_servers: str, group_id: str, topic: str) -> MessageSubscriber:
        return KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id=group_id, topic=topic)


class PubSubPublisherCreator(MessageSubscriberCreator):
    def create_publisher(self, **kwargs) -> MessageSubscriber:
        return PubSubSubscriber(**kwargs)
