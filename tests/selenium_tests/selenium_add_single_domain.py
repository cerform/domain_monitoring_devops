from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pytest

BASE_URL = "http://localhost:8080"

@pytest.fixture
def driver():
    """
    Creating a Chrome WebDriver  instance
    """
    options = options()

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()
    


