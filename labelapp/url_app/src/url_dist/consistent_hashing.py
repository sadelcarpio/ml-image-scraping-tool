import logging

from sqlalchemy.orm.query import Query

from src.utils import sha256_hash

logger = logging.getLogger(__name__)


class ConsistentHashing:
    def __init__(self, n_hash_ring: int = 1000):
        self.n_hash_ring = n_hash_ring

    def distribute_url(self, hashed_url, user_ids: list) -> str:
        ring_position = int(hashed_url, 16) % self.n_hash_ring
        logger.info(f"GCS URL on position {ring_position}/{self.n_hash_ring}.")
        user_ring_positions = self._get_sorted_ring_positions(user_ids)
        user_id = None
        current = 0
        while not user_id:
            if not len(user_ids):
                break
            elif current == len(user_ids):
                user_id = user_ring_positions[current - 1][0]
                logger.info(f"Assigned {ring_position} to user {user_ring_positions[current - 1][0]}"
                            f" in position {user_ring_positions[current - 1][1]}")
            elif ring_position >= user_ring_positions[current][1]:
                current += 1
            else:
                logger.info(f"Assigned {ring_position} to user {user_ring_positions[current - 1][0]}"
                            f" in position {user_ring_positions[current - 1][1]}")
                user_id = user_ring_positions[current - 1][0]
        return user_id

    def _get_sorted_ring_positions(self, query: list) -> list:
        return sorted(map(lambda item: (item[0].hex, int(sha256_hash(item[0].hex), 16) % self.n_hash_ring), query),
                      key=lambda x: x[1])
