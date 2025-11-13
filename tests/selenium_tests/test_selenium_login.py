from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_login_page():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8080/login")

    assert "Login" in driver.title

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    submit = driver.find_element(By.ID, "login-button")

    username.send_keys("apitester")
    password.send_keys("Apitester1")
    submit.click()

    time.sleep(1)
    assert "Dashboard" in driver.title

    driver.quit()
