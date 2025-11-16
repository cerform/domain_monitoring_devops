import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from selenium.webdriver.common.by import By

# --------
# Positive test: valid login
# --------
def test_login_valid(driver):
    login_page = LoginPage(driver)

    # Go to login page
    login_page.load()

    # Perform login
    login_page.login("john_doe", "password")

    # Assert by title
    assert "dashboard" in driver.title.lower()

# --------
# Negative tests: invalid login
# --------
@pytest.mark.parametrize(
    "username,password",
    [
        ("john_doe", "wrong_password"),
        ("wrong_user", "password"),
        ("", "password"),
        ("john_doe", ""),
        ("", ""),
    ],
)
def test_login_invalid(driver, username, password):
    login_page = LoginPage(driver)

    login_page.load()
    login_page.login(username, password)

    # You need some stable way to detect "login failed".
    # Example: an error div with id="error-message" and text with "Invalid".
    # Update the locator/text below to match your real HTML.

    error_locator = (By.ID, "failed-login")  # change if needed

    # Check for error message visibility and content
    assert login_page.get_text(error_locator) == "Login failed"
    assert login_page.is_visible(error_locator)

    # Extra safety: user should *not* be on dashboard
    assert "dashboard" not in driver.title.lower()
