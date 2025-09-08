import json

class UserManager:
    def __init__(self):
        pass

    def register_user(self, username, password): ## Add user to json file
        with open('/userdata/users.json', 'r') as f:
            users = json.load(f)
        if username in users:
            return False  # User already exists
        users[username] = password
        with open('/userdata/users.json', 'w') as f:
            json.dump(users, f)
        return True

    def validate_login(self, username, password):
        with open('/userdata/users.json', 'r') as f:
            users = json.load(f)
        if username in users and users[username] == password:
            return True
        return False