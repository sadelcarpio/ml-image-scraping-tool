import logging
import os

from url_app.db.session import PostgreSQLSessionCreator
from url_app.kafka.consumer import KafkaConsumer

logging.basicConfig(level=logging.INFO)


def main():
    sql_session = PostgreSQLSessionCreator().create_session()
    consumer = KafkaConsumer(bootstrap_servers=os.environ["KAFKA_LISTENER"], group_id='read-urls',
                             topic=os.environ["MSG_TOPIC"], sql_session=sql_session)
    consumer.read_urls()


if __name__ == '__main__':
    main()
