import logging
import os

from src.db.db_operations import PostgreSQLSessionCreator
from src.kafka.consumer import KafkaConsumer

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    sql_session = PostgreSQLSessionCreator().create_session()
    consumer = KafkaConsumer(bootstrap_servers=os.environ["KAFKA_LISTENER"], group_id='read-urls',
                             topic=os.environ["MSG_TOPIC"], db_session=sql_session)
    consumer.read_urls()
