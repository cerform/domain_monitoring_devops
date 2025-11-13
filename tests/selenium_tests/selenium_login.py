from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_login(driver):
    # Wait for login button
    btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.login"))
    )
    assert btn is not None, "Login button not found"

    btn.click()

    # Wait for login form
    form = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "login-form"))
    )
    assert form is not None, "Login form did not appear"

    # Fields
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    assert username is not None, "Username field missing"
    assert password is not None, "Password field missing"

    # Fill form
    username.send_keys("john_doe")
    password.send_keys("password" + Keys.RETURN)

    # Validate login (change selector to your success UI)
    dashboard = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "dashboard"))
    )
    assert dashboard is not None, "Dashboard did not load after login"

    return True   # optional, pytest doesn't need it
