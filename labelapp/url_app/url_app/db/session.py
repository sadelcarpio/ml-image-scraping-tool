import os
from abc import abstractmethod

from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from url_app.db.base import Base
from url_app.db.db_operations import SQLSession


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
            user=f"{os.environ['POSTGRES_USER']}",
            password=f"{os.environ['POSTGRES_PASSWORD']}",
            db=f"{os.environ['POSTGRES_DB']}"
        )
        return conn


class PostgreSQLSessionCreator(SQLSessionCreator):
    def create_session(self) -> SQLSession:
        """Creates a Session to connect to an arbitrary Postgres instance"""
        engine = create_engine(f"postgresql+pg8000://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
                               f"@{os.environ['INSTANCE_NAME']}/{os.environ['POSTGRES_DB']}")
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        return SQLSession(session)
