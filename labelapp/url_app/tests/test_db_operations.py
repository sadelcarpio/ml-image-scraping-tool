import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy import exc

from url_app.db.db_operations import SQLSession
from sqlalchemy.orm.session import sessionmaker, Session


class TestSQLOperations(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock(spec=sessionmaker)
        self.db = MagicMock(spec=Session)
        self.mock_session.return_value = self.db
        self.sql_session = SQLSession(session=self.mock_session)
        self.dist_strategy = MagicMock()

    @patch('url_app.db.db_operations.UrlModel')
    def test_upload_url(self, mock_url_model):
        self.db.query.return_value.join.return_value.filter_by.return_value.all.return_value = ['uid1', 'uid2', 'uid3']
        self.dist_strategy.distribute_url.return_value = 'uid1'
        self.db.query.return_value.filter_by.return_value.first.return_value.id = 1234
        self.sql_session.upload_url('https://storage.googleapis/nolose.jpg',
                                    'abcdef',
                                    'test-project',
                                    self.dist_strategy)
        self.mock_session.assert_called_once()
        mock_url_model.assert_called_once_with(gcs_url='https://storage.googleapis/nolose.jpg',
                                               hashed_url='abcdef', labeled=False, project_id=1234, user_id='uid1')
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.db.close.assert_called_once()

    def test_upload_url_integrity_error(self):
        self.db.commit.side_effect = exc.IntegrityError("Record already exists.", [], BaseException())
        self.sql_session.upload_url('https://storage.googleapis/nolose.jpg',
                                    'abcdef',
                                    'test-project',
                                    self.dist_strategy)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()

    def test_upload_url_sqlalchemyerror(self):
        self.db.commit.side_effect = exc.SQLAlchemyError("Some error happened")
        with self.assertRaises(exc.SQLAlchemyError):
            self.sql_session.upload_url('https://storage.googleapis/nolose.jpg',
                                        'abcdef',
                                        'test-project',
                                        self.dist_strategy)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()

    def test_user_deleted(self):
        # Normal behavior
        self.db.query.return_value.join.return_value.filter_by.return_value.all.return_value = ['uid1', 'uid2', 'uid3']
        mock_reassign_unlabeled_urls = MagicMock()
        self.sql_session.reassign_unlabeled_urls = mock_reassign_unlabeled_urls
        self.sql_session.upload_url('https://storage.googleapis/nolose.jpg',
                                    'abcdef',
                                    'test-project',
                                    self.dist_strategy)
        self.assertEqual(3, self.sql_session.n_users)
        # Now as if one user were deleted
        self.db.query.return_value.join.return_value.filter_by.return_value.all.return_value = ['uid1', 'uid3']
        self.sql_session.upload_url('https://storage.googleapis/silose.jpg',
                                    '12345',
                                    'test-project',
                                    self.dist_strategy)
        self.assertEqual(2, self.sql_session.n_users)
        self.sql_session.reassign_unlabeled_urls.assert_called_once_with(['uid1', 'uid3'],
                                                                         self.dist_strategy)
        self.assertEqual(2, len(self.dist_strategy.distribute_url.call_args_list))

    def test_reassign_unlabeled_urls(self):
        user_ids = ['uid1', 'uid2', 'uid3']
        self.dist_strategy.distribute_url.side_effect = ['uid1', 'uid2']
        mock_url_1 = MagicMock(hashed_url='123')
        mock_url_2 = MagicMock(hashed_url='abc')
        self.db.query.return_value.filter_by.return_value = [mock_url_1, mock_url_2]
        self.sql_session.reassign_unlabeled_urls(user_ids, self.dist_strategy)
        self.assertEqual(2, len(self.dist_strategy.distribute_url.call_args_list))
        self.assertEqual(2, len(self.db.commit.call_args_list))
        self.assertEqual(2, len(self.db.refresh.call_args_list))
        self.assertEqual('uid1', mock_url_1.user_id)
        self.assertEqual('uid2', mock_url_2.user_id)

    def test_reassign_urls_sqlalchemyerror(self):
        self.db.commit.side_effect = exc.SQLAlchemyError("Another error happened")
        self.db.query.return_value.filter_by.return_value = [MagicMock(hashed_url='123'), MagicMock(hashed_url='abc')]
        with self.assertRaises(exc.SQLAlchemyError):
            self.sql_session.reassign_unlabeled_urls(['uid1', 'uid2'], self.dist_strategy)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()
