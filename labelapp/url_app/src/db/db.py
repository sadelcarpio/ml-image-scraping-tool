from abc import abstractmethod

import sqlalchemy.engine.base
from google.cloud.sql.connector import Connector
import os

from sqlalchemy import create_engine


class SQLConn:
    def __init__(self, pool):
        self.pool = pool

    def save(self, values):
        pass


class CloudSQLConn(SQLConn):

    def save(self, values):
        pass


class PostgreSQLConn(SQLConn):

    def save(self, values):
        pass


class SQLConnCreator:
    @abstractmethod
    def create_conn(self):
        pass


class CloudSQLConnCreator(SQLConnCreator):
    def create_conn(self) -> CloudSQLConn:
        return CloudSQLConn(create_engine("postgresql+pg8000://", creator=self.getconn()))

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


class PostgreSQLConnCreator(SQLConnCreator):
    def create_conn(self) -> SQLConn:
        return PostgreSQLConn(create_engine("postgresql+pg8000://"))  # Missing some conn parameters
