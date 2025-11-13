from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import selenium_register
import selenium_login
import selenium_single_domain
import selenium_bulk_domain
import pytest

def create_linux_driver():
    options = Options()

    # use the one that actually exists on your system:
    options.binary_location = "/usr/bin/chromium-browser"  # or "/usr/bin/chromium"

    # headless etc.
    # options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    # again: match what `which chromedriver` gave you
    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)

def test_master():
    driver = create_linux_driver()
    # Connect to the web application
    driver.get("http://127.0.0.1:8080/")
    # Check if the app is online
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Web application is online.")
    except Exception as e:
        print(f"Error: Web application is not reachable. {e}")
        driver.quit()
        exit(1)
    # Test registration functionality
    selenium_register.register(driver)
    # Test login functionality
    selenium_login.test_login(driver)
    # Test add single domain functionality
    selenium_single_domain.add_single_domain(driver)
    # Test add bulk domains functionality
    selenium_bulk_domain.add_bulk_domains(driver)

    time.sleep(10)
    driver.quit()
