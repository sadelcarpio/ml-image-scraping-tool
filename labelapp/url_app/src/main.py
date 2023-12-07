from src.kafka.consumer import KafkaConsumer

if __name__ == '__main__':
    consumer = KafkaConsumer(bootstrap_servers="kafka-service:19092", group_id='read-urls', topic='google-images')
    consumer.read_urls()
