import json

import logging

from url_app.db.db_operations import SQLSession
from url_app.events.subscribe import MessageSubscriber
from url_app.url_dist import VirtualNodesConsistentHashing
from url_app.utils import sha256_hash

logger = logging.getLogger(__name__)


class UrlHandler:
    def __init__(self, sql_session: SQLSession, message_subscriber: MessageSubscriber):
        self.sql_session = sql_session
        self.strategy = VirtualNodesConsistentHashing(n_hash_ring=1000, num_replicas=10)
        self.message_subscriber = message_subscriber

    def read_urls(self):
        try:
            while True:
                msg = self.message_subscriber.receive_url()
                if msg is None:
                    logger.info("Waiting ...")
                elif msg.error():
                    logger.warning(f"ERROR: {msg.error()}")
                else:
                    decoded_msg = json.loads(msg.value().decode('utf-8'))
                    gcs_url, project_name = decoded_msg['url'], decoded_msg['project']
                    hashed_url = sha256_hash(gcs_url)
                    logger.info(f"Consumed event from topic {self.message_subscriber.topic}: "
                                f"url = {gcs_url}, project = {project_name}")
                    self.sql_session.upload_url(gcs_url=gcs_url,
                                                hashed_url=hashed_url,
                                                project_name=project_name,
                                                dist_strategy=self.strategy)
        finally:
            self.message_subscriber.client.close()
