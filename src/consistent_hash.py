import hashlib
import bisect

class ConsistentHash:
    # Initialize the consistent hash ring with given slots and virtual servers
    def __init__(self, num_slots=512, num_virtual_servers=9):
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.ring = []
        self.server_map = {}

    def _hash(self, key):
        # Compute the hash value of the given key using SHA-256 and reduce it to the range of num_slots
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % self.num_slots

    def add_server(self, server_id):
        # Add a server and its virtual nodes to the hash ring
        for i in range(self.num_virtual_servers):
            virtual_node_key = f"{server_id}-{i}"
            hash_value = self._hash(virtual_node_key)
            bisect.insort(self.ring, hash_value)
            self.server_map[hash_value] = server_id

    def remove_server(self, server_id):
        # Remove a server and its virtual nodes from the hash ring
        for i in range(self.num_virtual_servers):
            virtual_node_key = f"{server_id}-{i}"
            hash_value = self._hash(virtual_node_key)
            index = bisect.bisect_left(self.ring, hash_value)
            if index < len(self.ring) and self.ring[index] == hash_value:
                self.ring.pop(index)
                del self.server_map[hash_value]

    def get_server(self, key):
        # Get the server that should handle the given key
        if not self.ring:
            return None
        hash_value = self._hash(key)
        index = bisect.bisect_left(self.ring, hash_value)
        if index == len(self.ring):
            index = 0
        return self.server_map[self.ring[index]]

# Example usage
if __name__ == "__main__":
    ch = ConsistentHash()
    ch.add_server("Server1")
    ch.add_server("Server2")
    ch.add_server("Server3")

    print(ch.get_server("ClientRequest1"))
    print(ch.get_server("ClientRequest2"))
    print(ch.get_server("ClientRequest3"))
