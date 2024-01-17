import json
import logging

import confluent_kafka

from url_app.db.db_operations import SQLSession
from url_app.url_dist import VirtualNodesConsistentHashing
from url_app.utils import sha256_hash

logger = logging.getLogger(__name__)


class KafkaConsumer(confluent_kafka.Consumer):
    def __init__(self, bootstrap_servers: str, group_id: str, topic: str, sql_session: SQLSession):
        super().__init__({'bootstrap.servers': bootstrap_servers, 'group.id': group_id})
        self.topic = topic
        self.subscribe([self.topic])
        self.sql_session = sql_session
        self.strategy = VirtualNodesConsistentHashing(n_hash_ring=1000, num_replicas=10)

    def read_urls(self):
        try:
            while True:
                msg = self.poll(1.0)
                if msg is None:
                    logger.info("Waiting ...")
                elif msg.error():
                    logger.warning(f"ERROR: {msg.error()}")
                else:
                    decoded_msg = json.loads(msg.value().decode('utf-8'))
                    gcs_url, project_name = decoded_msg['url'], decoded_msg['project']
                    hashed_url = sha256_hash(gcs_url)
                    logger.info(f"Consumed event from topic {self.topic}: url = {gcs_url}, project = {project_name}")
                    self.sql_session.upload_url(gcs_url=gcs_url,
                                                hashed_url=hashed_url,
                                                project_name=project_name,
                                                dist_strategy=self.strategy)
        finally:
            self.close()
