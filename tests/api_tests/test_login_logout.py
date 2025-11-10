from Aux_Library import check_login_user
import pytest

# Check valid login
def test_login_valid():
    login_result = check_login_user("john_doe", "password")
    assert login_result.status_code == 200 
    assert login_result.json().get("message") == "Login successful"
    assert login_result.json().get("username") == "john_doe"

@pytest.mark.parametrize("username,password", [
    ("JOHN_DOE", "PASSWORD"),   # case-sensitive mismatch
    ("john_doe", "wrong_password"),  # wrong password
    ("wrong_username", "password"),  # wrong username
    ("", "password"),                # empty username
    ("john_doe", ""),                # empty password
    ("", ""),                        # both empty
])

# Check invalid login scenarios
def test_login_invalid(username, password):
    login_result = check_login_user(username, password)
    assert login_result.status_code == 401 
    assert login_result.json().get("error") == "Invalid username or password"