import logging
import os
from abc import abstractmethod

from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from src.db import models
from src.db.base import Base

logger = logging.getLogger(__name__)


class SQLSession:
    def __init__(self, session: sessionmaker):
        self.session = session

    def upload_url(self, gcs_url):
        db = self.session()
        try:
            db_url = models.UrlModel(gcs_url=gcs_url)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
        except exc.IntegrityError:
            logger.error(f"The value already exists in the database.")
            db.rollback()
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to upload: {e}")
            db.rollback()
            raise
        finally:
            db.close()


class CloudSQLSession(SQLSession):
    pass


class PostgreSQLSession(SQLSession):
    pass


class SQLSessionCreator:
    @abstractmethod
    def create_session(self):
        pass


class CloudSQLSessionCreator(SQLSessionCreator):
    def create_session(self) -> CloudSQLSession:
        engine = create_engine("postgresql+pg8000://", creator=self.getconn)
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        return CloudSQLSession(session)

    @staticmethod
    def getconn():
        connector = Connector()
        conn = connector.connect(
            f"{os.environ['PROJECT_ID']}:{os.environ['DB_REGION']}:{os.environ['INSTANCE_NAME']}",
            "pg8000",
            user=f"{os.environ['DB_USER']}",
            password=f"{os.environ['DB_PASSWORD']}",
            db=f"{os.environ['DB_NAME']}"
        )
        return conn


class PostgreSQLSessionCreator(SQLSessionCreator):
    def create_session(self) -> SQLSession:
        engine = create_engine(f"postgresql+pg8000://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
                               f"@{os.environ['INSTANCE_NAME']}/{os.environ['DB_NAME']}")
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        return PostgreSQLSession(session)
