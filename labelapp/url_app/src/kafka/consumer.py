import logging

import confluent_kafka

from src.db.db_operations import SQLSession
from src.url_dist import VirtualNodesConsistentHashing
from src.utils import sha256_hash

logger = logging.getLogger(__name__)


class KafkaConsumer(confluent_kafka.Consumer):
    def __init__(self, bootstrap_servers: str, group_id: str, topic: str, db_session: SQLSession):
        super().__init__({'bootstrap.servers': bootstrap_servers, 'group.id': group_id})
        self.topic = topic
        self.subscribe([self.topic])
        self.db_session = db_session
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
                    gcs_url = msg.value().decode('utf-8')
                    hashed_url = sha256_hash(gcs_url)
                    logger.info(f"Consumed event from topic {self.topic}: value = "
                                f"{gcs_url}")
                    self.db_session.upload_url(gcs_url=gcs_url,
                                               hashed_url=hashed_url,
                                               dist_strategy=self.strategy)
        finally:
            self.close()
