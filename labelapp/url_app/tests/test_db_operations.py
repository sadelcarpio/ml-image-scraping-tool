import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy import exc

from src.db.db_operations import SQLSession


class TestSQLOperations(unittest.TestCase):

    def setUp(self):
        mock_session = MagicMock()
        self.db = MagicMock()
        self.dist_strategy = MagicMock()
        self.dist_strategy.distribute_url.return_value = 'uid1'
        mock_session.return_value = self.db
        self.db.query.return_value.all.return_value = ['uid1', 'uid2', 'uid3']
        self.db_session = SQLSession(session=mock_session)

    @patch('src.db.models.UrlModel')
    def test_upload_url(self, mock_url_model):
        self.db_session.upload_url('https://storage.googleapis/nolose.jpg', 'abcdef', self.dist_strategy)
        self.db_session.session.assert_called_once()
        mock_url_model.assert_called_once_with(gcs_url='https://storage.googleapis/nolose.jpg',
                                               hashed_url='abcdef', labeled=False, user_id='uid1')
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.db.close.assert_called_once()

    def test_upload_url_integrity_error(self):
        self.db.commit.side_effect = exc.IntegrityError("Record already exists.", [], BaseException())
        self.db_session.upload_url('https://storage.googleapis/nolose.jpg', 'abcdef', self.dist_strategy)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()

    def test_upload_url_sqlalchemyerror(self):
        self.db.commit.side_effect = exc.SQLAlchemyError("Some error happened")
        with self.assertRaises(exc.SQLAlchemyError):
            self.db_session.upload_url('https://storage.googleapis/nolose.jpg', 'abcdef', self.dist_strategy)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()

    def test_user_deleted(self):
        mock_reassign_unlabeled_urls = MagicMock()
        self.db_session.reassign_unlabeled_urls = mock_reassign_unlabeled_urls
        self.db_session.upload_url('https://storage.googleapis/nolose.jpg', 'abcdef', self.dist_strategy)
        self.assertEqual(3, self.db_session.n_users)
        self.db.query.return_value.all.return_value = ['uid1', 'uid3']
        self.db_session.upload_url('https://storage.googleapis/silose.jpg', '12345', self.dist_strategy)
        self.assertEqual(2, self.db_session.n_users)
        self.db_session.reassign_unlabeled_urls.assert_called_once_with(['uid1', 'uid3'],
                                                                        self.dist_strategy)
        self.assertEqual(2, len(self.dist_strategy.distribute_url.call_args_list))

    def test_reassign_unlabeled_urls(self):
        user_ids = ['uid1', 'uid2', 'uid3']
        self.dist_strategy.distribute_url.side_effect = ['uid1', 'uid2']
        mock_url_1 = MagicMock(hashed_url='123')
        mock_url_2 = MagicMock(hashed_url='abc')
        self.db.query.return_value.filter_by.return_value = [mock_url_1, mock_url_2]
        self.db_session.reassign_unlabeled_urls(user_ids, self.dist_strategy)
        self.assertEqual(2, len(self.dist_strategy.distribute_url.call_args_list))
        self.assertEqual(2, len(self.db.commit.call_args_list))
        self.assertEqual(2, len(self.db.refresh.call_args_list))
        self.assertEqual('uid1', mock_url_1.user_id)
        self.assertEqual('uid2', mock_url_2.user_id)

    def test_reassign_urls_sqlalchemyerror(self):
        self.db.commit.side_effect = exc.SQLAlchemyError("Another error happened")
        self.db.query.return_value.filter_by.return_value = [MagicMock(hashed_url='123'), MagicMock(hashed_url='abc')]
        with self.assertRaises(exc.SQLAlchemyError):
            self.db_session.reassign_unlabeled_urls(['uid1', 'uid2'], self.dist_strategy)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_not_called()
        self.db.rollback.assert_called_once()
        self.db.close.assert_called_once()
