import json
import re

class UserManager:
    
    def register_page_add_user(self, username, password, password_confirmation):
        try:
            with open("./UsersData/users.json") as f:
                users = json.load(f)
            if not self.username_validity(users, username):
                return "FAILED", "Username is invalid!"
            password_validity = self.register_page_password_validity(password, password_confirmation)
            if password_validity[0] == "FAILED" or not password_validity[0]:
                return "FAILED", password_validity[1]
            write_user_status = self.write_user_to_json(users, username, password)
            if write_user_status[0] == "FAILED":
                return "FAILED", write_user_status[1]
            return "SUCCESS", "User registered Successfully!"
        except Exception as e:
            return "FAILED","Error: Unable to register user.", e

    def register_page_password_validity(self, password, password_confirmation):
        try:
            if password != password_confirmation:
                return False, "Password and Password Confirmation are not the same."
            password_str = f"{password}"
            if len(password_str) < 8 or len(password_str) > 12:
                return False, "Password is not between 8 to 12 characters."
            if not re.fullmatch("[A-Z]+", password_str):
                return False, "Password does not include at least one uppercase character."
            if not re.fullmatch("[a-z]+", password_str):
                return False, "Password does not include at least one lowercase character."
            if not re.fullmatch("[0-9]+", password_str):
                return False, "Password does not include at least one digit."
            if not password_str.isalnum():
                return False, "Password should include only uppercase \
                    characters, lowercase characters and digits!"
            return True, "SUCCESS"
        except Exception as e:
            return "FAILED", "Error: Unable to validate password.", e

    def username_validity(self, users_json, username):
        try:
            if f"{username}" in users_json:
                return False, "Username already Exists."
            return True, "Username is valid."
        except Exception as e:
            return "FAILED","Error: Unable to validate username.", e 
    
    def write_user_to_json(self, users_json,username, password):
        try:
            user_to_write = {
                f"{username}" : f"{password}"
            }
            users_json.update(user_to_write)
            return "SUCCESS", "Username and password was written successfully."
        except Exception as e:
            return "FAILED", "Error: Unable to write user to file.", e 


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