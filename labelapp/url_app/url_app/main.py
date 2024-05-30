import logging
import os

from url_app.db.session import PostgreSQLSessionCreator
from url_app.events.subscribe import KafkaConsumerCreator
from url_app.url_handler import UrlHandler

logging.basicConfig(level=logging.INFO)


def main():
    sql_session = PostgreSQLSessionCreator().create_session()
    subscriber = KafkaConsumerCreator().create_publisher(bootstrap_servers=os.environ["KAFKA_LISTENER"],
                                                         group_id="read-urls",
                                                         topic=os.environ["MSG_TOPIC"])
    handler = UrlHandler(sql_session=sql_session, message_subscriber=subscriber)
    handler.read_urls()


if __name__ == '__main__':
    main()
