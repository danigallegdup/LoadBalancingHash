"""
dgallegosdupuis@seng468-group9:~/LoadBalancingHash$ python3 normal_hashing.py 

Student ID -> (Server, Grade)
101 -> (S1, 88)
202 -> (S2, 92)
303 -> (S3, 75)
404 -> (S4, 81)
505 -> (S0, 89)

[INFO] Server S4 has failed. Reassigning grades...

New Assignments after Failure:
404 -> (S0, 81)
"""

class NormalHashing:
    def __init__(self, servers):
        self.servers = servers  # List of servers S0, S1, S2, S3, S4
    
    def hash_position(self, student_id):
        return student_id % 1000  # Hash position
    
    def assigned_server(self, student_id):
        return self.hash_position(student_id) % len(self.servers)  # Assign to a server

    def store_grades(self, student_grades):
        self.grade_map = {}  # Dictionary to store the mapping
        for student_id, grade in student_grades.items():
            server = self.assigned_server(student_id)
            self.grade_map[student_id] = (server, grade)
        return self.grade_map

    def display_mapping(self):
        print("\nStudent ID -> (Server, Grade)")
        for student_id, (server, grade) in self.grade_map.items():
            print(f"{student_id} -> (S{server}, {grade})")

    def handle_server_failure(self, failed_server):
        print(f"\n[INFO] Server S{failed_server} has failed. Reassigning grades...\n")
        new_assignments = {}
        remaining_servers = [s for s in range(len(self.servers)) if s != failed_server]

        for student_id, (server, grade) in list(self.grade_map.items()):
            if server == failed_server:
                new_server = remaining_servers[student_id % len(remaining_servers)]  # Evenly redistribute
                new_assignments[student_id] = (new_server, grade)
                self.grade_map[student_id] = (new_server, grade)  # Update main mapping

        print("New Assignments after Failure:")
        for student_id, (server, grade) in new_assignments.items():
            print(f"{student_id} -> (S{server}, {grade})")

# Example Student Data
grades = {101: 88, 202: 92, 303: 75, 404: 81, 505: 89}
normal_hash = NormalHashing(["S0", "S1", "S2", "S3", "S4"])
normal_hash.store_grades(grades)
normal_hash.display_mapping()

# Simulate failure of S4
normal_hash.handle_server_failure(4)
