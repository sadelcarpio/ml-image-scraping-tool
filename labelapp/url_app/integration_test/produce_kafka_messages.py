import json
import logging

import confluent_kafka
from sqlalchemy import exc

from url_app.db.models import UserModel, ProjectModel
from url_app.db.session import PostgreSQLSessionCreator

logger = logging.getLogger(__name__)

sql_session = PostgreSQLSessionCreator().create_session()
db = sql_session.session()

try:
    user = UserModel()
    db.add(user)
    db.commit()
    db.refresh(user)
    project = ProjectModel(name="test-project")
    project.users = [user]
    db.add(project)
    db.commit()
    db.refresh(project)
except exc.SQLAlchemyError as e:
    logger.error(f"Could not perform operations. {e}")

producer = confluent_kafka.Producer({'bootstrap.servers': "kafka-service:19092",
                                     "client.id": "integration-test-client"})

msg = {"url": "https://storage.googleapis.com/{folder}/{filename}", "project": "test-project"}
producer.produce(topic="google-images", value=bytes(json.dumps(msg).encode('utf-8')))
