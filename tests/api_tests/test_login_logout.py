import Aux_Library
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

# Test connectivity to pages
# response_root = Aux_Library.check_get_webpage("/")
# response_login = Aux_Library.check_get_webpage("/login")
# response_register = Aux_Library.check_get_webpage("/register")

# Test user registration
# registration_result = Aux_Library.check_register_user("testuser", "Testpass123", "Testpass123")

# Test user login
login_result = Aux_Library.check_login_user("john_doe", "password")
session = login_result.cookies["session"]

# Extract session cookie for further authenticated requests

print(session)