import os

from src.db.database import CloudSQLSessionCreator
from src.kafka.consumer import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    sql_session = CloudSQLSessionCreator().create_session()
    consumer = KafkaConsumer(bootstrap_servers=os.environ["KAFKA_LISTENER"], group_id='read-urls',
                             topic=os.environ["MSG_TOPIC"], db_session=sql_session)
    consumer.read_urls()
