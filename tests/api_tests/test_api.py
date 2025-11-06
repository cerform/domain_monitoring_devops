import api_tester

# Test connectivity to pages
response_root = api_tester.test_get_webpage("/")
response_login = api_tester.test_get_webpage("/login")
response_register = api_tester.test_get_webpage("/register")

# Test user registration
registration_result = api_tester.test_register_user("testuser", "Testpass123", "Testpass123")

# Test user login
login_result = api_tester.test_login_user("testuser", "Testpass123")
# Extract session cookie for further authenticated requests
session = login_result["session"]

# Test dashboard content
response_dashboard = api_tester.check_dashboard(session)
print(response_dashboard)
