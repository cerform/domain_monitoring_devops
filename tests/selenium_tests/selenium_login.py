from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def login(driver, username, password):
    WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "btn.login"))
)
    # Find the login button
    login_button = driver.find_element(By.CLASS_NAME, "btn.login")
    # Click the login button
    login_button.click()