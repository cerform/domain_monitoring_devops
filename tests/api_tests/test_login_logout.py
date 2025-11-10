import Aux_Library
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

# Test connectivity to pages
response_root = Aux_Library.test_get_webpage("/")
response_login = Aux_Library.test_get_webpage("/login")
response_register = Aux_Library.test_get_webpage("/register")

# Test user registration
registration_result = Aux_Library.test_register_user("testuser", "Testpass123", "Testpass123")

# Test user login
login_result = Aux_Library.test_login_user("testuser", "Testpass123")
# Extract session cookie for further authenticated requests
session = login_result["session"]

# Test dashboard content
response_dashboard = Aux_Library.check_dashboard(session)
print(response_dashboard)
