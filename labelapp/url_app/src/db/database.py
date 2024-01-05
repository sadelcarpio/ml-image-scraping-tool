import logging
import os
from abc import abstractmethod

from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from src.db import models
from src.db.base import Base
from src.url_dist import ConsistentHashing

logger = logging.getLogger(__name__)


class SQLSession:
    def __init__(self, session: sessionmaker):
        self.session = session
        self.n_users = None

    def upload_url(self, gcs_url: str, hashed_url: str, dist_strategy: ConsistentHashing):
        db = self.session()
        try:
            user_ids = db.query(models.UserModel.id).all()
            if self.n_users is None:
                self.n_users = len(user_ids)
            if len(user_ids) < self.n_users:
                logger.info("A user was deleted, reassigning orphan URLs ...")
                # Could add a custom exception here to move this logic to consumer level
                self.reassign_unlabeled_urls(user_ids, dist_strategy)
                logger.info("Orphan URLs reassigned.")
                self.n_users = len(user_ids)
            user_id = dist_strategy.distribute_url(hashed_url, user_ids)
            db_url = models.UrlModel(gcs_url=gcs_url, hashed_url=hashed_url, labeled=False, user_id=user_id)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
        except exc.IntegrityError:
            logger.error(f"The GCS URL: {gcs_url} already exists in the database.")
            db.rollback()
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to upload: {e}")
            db.rollback()
            raise
        finally:
            db.close()

    def reassign_unlabeled_urls(self, user_ids: list, dist_strategy: ConsistentHashing):
        db = self.session()
        try:
            unlabeled_urls = db.query(models.UrlModel).filter_by(labeled=False, user_id=None)
            for db_url in unlabeled_urls:
                user_id = dist_strategy.distribute_url(db_url.hashed_url, user_ids)
                if user_id is None:
                    return
                db_url.user_id = user_id
                db.commit()
                db.refresh(db_url)
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to upload: {e}")
            db.rollback()
            raise


class SQLSessionCreator:
    @abstractmethod
    def create_session(self) -> SQLSession:
        """Creates a SQLSession object that holds a SQLAlchemy session in order to be used alongside the ORM"""
        pass


class CloudSQLSessionCreator(SQLSessionCreator):
    def create_session(self) -> SQLSession:
        """Creates a SQLSession to connect to a CloudSQL instance, using CloudSQL Python Connector"""
        engine = create_engine("postgresql+pg8000://", creator=self.getconn)
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        return SQLSession(session)

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
        """Creates a Session to connect to an arbitrary Postgres instance"""
        engine = create_engine(f"postgresql+pg8000://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
                               f"@{os.environ['INSTANCE_NAME']}/{os.environ['DB_NAME']}")
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        return SQLSession(session)
