import logging
import unittest
from datetime import datetime

from sqlalchemy import exc

from integration_test.setup import URLS as EXPECTED_URLS
from url_app.db.models import UrlModel
from url_app.db.session import PostgreSQLSessionCreator

logger = logging.getLogger(__name__)

sql_session = PostgreSQLSessionCreator().create_session()
db = sql_session.session()


class UrlAppIntegrationTest(unittest.TestCase):

    def test_url_in_db(self):
        try:
            urls = db.query(UrlModel).all()
            for url, expected_url in zip(urls, EXPECTED_URLS):
                self.assertEqual(expected_url, url.gcs_url)
                self.assertIsNotNone(url.user_id)
                self.assertEqual(1, url.project_id)
                self.assertIsInstance(url.created_at, datetime)
                self.assertIsInstance(url.updated_at, datetime)
        except exc.SQLAlchemyError as e:
            logger.error(f"Could not perform operations. {e}")
            raise
        finally:
            db.close()
