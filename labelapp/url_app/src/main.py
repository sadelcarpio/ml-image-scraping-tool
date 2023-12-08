import os
from src.db.db import CloudSQLConnCreator
from src.kafka.consumer import KafkaConsumer

if __name__ == '__main__':
    cloud_sql_conn = CloudSQLConnCreator().create_conn()
    consumer = KafkaConsumer(bootstrap_servers="kafka-service:19092",
                             group_id='read-urls',
                             topic=os.environ["MSG_TOPIC"],
                             db_conn=cloud_sql_conn)
    consumer.read_urls()
