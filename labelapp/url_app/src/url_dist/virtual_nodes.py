from src.url_dist import ConsistentHashing
from src.utils import sha256_hash


class VirtualNodesConsistentHashing(ConsistentHashing):

    def __init__(self, n_hash_ring, num_replicas):
        super().__init__(n_hash_ring=n_hash_ring)
        self.num_replicas = num_replicas

    def _get_sorted_ring_positions(self, query: list) -> list:
        virtual_nodes = [(item[0].hex, int(sha256_hash(item[0].hex + str(i)), 16) % self.n_hash_ring) for item in query for i
                         in range(self.num_replicas)]
        return sorted(virtual_nodes, key=lambda x: x[1])
