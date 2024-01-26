import json
import logging
import os

import confluent_kafka
from sqlalchemy import exc

from url_app.db.models import UserModel, ProjectModel
from url_app.db.session import PostgreSQLSessionCreator

TOPIC_NAME = "google-images"

URLS = ["https://storage.googleapis.com/test_img1.jpg",
        "https://storage.googleapis.com/test_img2.jpg",
        "https://storage.googleapis.com/test_img3.jpg"]

PROJECT_NAME = "test-project"

logger = logging.getLogger(__name__)


def populate_db():
    sql_session = PostgreSQLSessionCreator().create_session()
    db = sql_session.session()
    try:
        user = UserModel()
        db.add(user)
        db.commit()
        db.refresh(user)
        project = ProjectModel(name=PROJECT_NAME)
        project.users = [user]
        db.add(project)
        db.commit()
        db.refresh(project)
    except exc.SQLAlchemyError as e:
        logger.error(f"Could not perform operations. {e}")
        raise
    finally:
        db.close()


def produce_msgs_to_kafka_topic():
    producer = confluent_kafka.Producer({'bootstrap.servers': os.environ["KAFKA_LISTENER"],
                                         "client.id": "integration-test-client"})
    for url in URLS:
        msg = {"url": url, "project": PROJECT_NAME}
        producer.produce(topic=TOPIC_NAME, value=bytes(json.dumps(msg).encode('utf-8')))
    producer.flush()


if __name__ == '__main__':
    populate_db()
    produce_msgs_to_kafka_topic()
