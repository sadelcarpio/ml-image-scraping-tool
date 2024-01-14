import unittest
from unittest.mock import MagicMock, patch

from url_app.url_dist import ConsistentHashing, VirtualNodesConsistentHashing


class TestConsistentHashing(unittest.TestCase):

    def test_distribute_url(self):
        dist_strategy = ConsistentHashing(n_hash_ring=100)
        hashed_urls = ['7903c0b0d7d3b873c5bedbed46c1d30435a269db6f0e6f35da48b02854cc4093',
                       'bff373de5b1cd16e0e10fdb1619d8c17c4b3fd51a2e7b428c76eed0518c653a7',
                       'b305e1123bc8070f0a0394355b067504c787ed4672355f709fc677c1f1cb8495',
                       '06113e1085ec5ad806b42c14d057ec6125541bf50d3f76075797121678eb586f',
                       '8cc524988207939e37741c77ac741f1335c3ebdce54dfbb913f51cb61008dfbf']
        user_mocks = [(MagicMock(),) for _ in range(5)]
        user_ids = ['bede18a1-15a5-4f28-883c-75f542f28843', 'f713e67d-284d-4db9-919f-83436212647d',
                    '8b9ecf5d-b2bf-4951-9657-6841778e1c0b', 'c9377141-e532-4d6b-b9a2-f271c17bc5da',
                    '818c77ca-a57a-41bd-96dc-9db69ad6e9e1']
        for mock, user_id in zip(user_mocks, user_ids):
            mock[0].configure_mock(hex=user_id)

        for hashed_url in hashed_urls:
            user_id = dist_strategy.distribute_url(hashed_url, user_mocks)
            self.assertIsInstance(user_id, str)
            self.assertIn(user_id, user_ids)

    @patch.object(ConsistentHashing, '_get_sorted_ring_positions')
    def test_user_id_assignment(self, mock_user_ring):
        dist_strategy = ConsistentHashing(n_hash_ring=10)
        hashed_urls = ['0', '2', '3', '4', '7', '8']
        user_ids = ['uid1', 'uid2', 'uid3']
        mock_user_ring.return_value = [('uid1', 2), ('uid2', 6), ('uid3', 8)]
        expected_user_ids = ['uid3', 'uid1', 'uid1', 'uid1', 'uid2', 'uid3']
        for hashed_url, expected_user_id in zip(hashed_urls, expected_user_ids):
            actual_user_id = dist_strategy.distribute_url(hashed_url, user_ids)
            self.assertEqual(expected_user_id, actual_user_id)

    def test_virtual_nodes(self):
        dist_strategy = VirtualNodesConsistentHashing(n_hash_ring=100, num_replicas=5)
        hashed_urls = ['7903c0b0d7d3b873c5bedbed46c1d30435a269db6f0e6f35da48b02854cc4093',
                       'bff373de5b1cd16e0e10fdb1619d8c17c4b3fd51a2e7b428c76eed0518c653a7',
                       'b305e1123bc8070f0a0394355b067504c787ed4672355f709fc677c1f1cb8495',
                       '06113e1085ec5ad806b42c14d057ec6125541bf50d3f76075797121678eb586f',
                       '8cc524988207939e37741c77ac741f1335c3ebdce54dfbb913f51cb61008dfbf']
        user_mocks = [(MagicMock(),) for _ in range(5)]
        user_ids = ['bede18a1-15a5-4f28-883c-75f542f28843', 'f713e67d-284d-4db9-919f-83436212647d',
                    '8b9ecf5d-b2bf-4951-9657-6841778e1c0b', 'c9377141-e532-4d6b-b9a2-f271c17bc5da',
                    '818c77ca-a57a-41bd-96dc-9db69ad6e9e1']
        for mock, user_id in zip(user_mocks, user_ids):
            mock[0].configure_mock(hex=user_id)

        for hashed_url in hashed_urls:
            user_id = dist_strategy.distribute_url(hashed_url, user_mocks)
            self.assertIsInstance(user_id, str)
            self.assertIn(user_id, user_ids)

    def test_virtual_nodes_assignment(self):
        dist_strategy = VirtualNodesConsistentHashing(n_hash_ring=1000, num_replicas=10)
        hashed_urls = ['0', '100', '200', '300', '400', '500', '600', '700', '800', '900']
        user_mocks = [(MagicMock(),) for _ in range(3)]
        user_ids = ['uid1', 'uid2', 'uid3']
        for mock, user_id in zip(user_mocks, user_ids):
            mock[0].configure_mock(hex=user_id)
        for hashed_url in hashed_urls:
            user_id = dist_strategy.distribute_url(hashed_url, user_mocks)
            self.assertIsInstance(user_id, str)
            self.assertIn(user_id, user_ids)

    def test_distribute_url_no_users(self):
        dist_strategy = ConsistentHashing(n_hash_ring=100)
        hashed_url = '7903c0b0d7d3b873c5bedbed46c1d30435a269db6f0e6f35da48b02854cc4093'
        user_id = dist_strategy.distribute_url(hashed_url, [])
        self.assertIsNone(user_id)
