"""
dgallegosdupuis@seng468-group9:~/LoadBalancingHash$ python3 consistent_hashing.py 

Student ID -> (Server, Grade)
101 -> (S3, 88)
202 -> (S3, 92)
303 -> (S0, 75)
404 -> (S0, 81)
505 -> (S2, 89)

[INFO] Server S2 has failed. Reassigning grades...


New Assignments after Failure:
505 -> (S1, 89)
"""


import bisect
import hashlib

class ConsistentHashing:
    def __init__(self, servers, num_virtual_nodes=3):
        self.num_virtual_nodes = num_virtual_nodes
        self.hash_ring = {}  # Stores (hashed_key -> server)
        self.sorted_keys = []  # Sorted list of hashed positions

        # Create multiple virtual nodes per server
        for server in servers:
            for i in range(num_virtual_nodes):
                server_hash = self.hash_function(f"{server}-vn{i}")  # Virtual nodes
                self.hash_ring[server_hash] = server
                self.sorted_keys.append(server_hash)

        # Sort the hash ring positions
        self.sorted_keys.sort()

    def hash_function(self, key):
        """ Use SHA-256 to distribute keys evenly """
        return int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % 1000000  # Mod large space

    def find_server(self, key):
        """ Find the next server in a clockwise direction """
        hashed_key = self.hash_function(key)
        index = bisect.bisect_right(self.sorted_keys, hashed_key)

        if index == len(self.sorted_keys):  # Wrap around if at the end
            index = 0

        return self.hash_ring[self.sorted_keys[index]]

    def store_grades(self, student_grades):
        """ Assign student grades to servers using consistent hashing """
        self.grade_map = {}
        for student_id, grade in student_grades.items():
            server = self.find_server(student_id)
            self.grade_map[student_id] = (server, grade)
        return self.grade_map

    def display_mapping(self):
        """ Print the assigned servers for each student """
        print("\nStudent ID -> (Server, Grade)")
        for student_id, (server, grade) in self.grade_map.items():
            print(f"{student_id} -> ({server}, {grade})")

    def handle_server_failure(self, failed_server):
        """ Remove a failed server and reassign its keys """
        print(f"\n[INFO] Server {failed_server} has failed. Reassigning grades...\n")

        # Remove virtual nodes of the failed server
        self.sorted_keys = [key for key in self.sorted_keys if self.hash_ring[key] != failed_server]
        self.hash_ring = {key: self.hash_ring[key] for key in self.sorted_keys}  # Update mapping

        # Reassign affected keys
        new_assignments = {}
        for student_id, (server, grade) in list(self.grade_map.items()):
            if server == failed_server:
                new_server = self.find_server(student_id)  # Find next available server
                new_assignments[student_id] = (new_server, grade)
                self.grade_map[student_id] = (new_server, grade)  # Update mapping

        print("\nNew Assignments after Failure:")
        for student_id, (server, grade) in new_assignments.items():
            print(f"{student_id} -> ({server}, {grade})")

# Example Data
servers = ["S0", "S1", "S2", "S3", "S4"]
grades = {101: 88, 202: 92, 303: 75, 404: 81, 505: 89}

# Initialize Consistent Hashing
consistent_hash = ConsistentHashing(servers)
consistent_hash.store_grades(grades)
consistent_hash.display_mapping()

# Simulate failure of S2
consistent_hash.handle_server_failure("S2")
