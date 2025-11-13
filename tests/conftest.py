import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    time.sleep(1)

    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return "http://localhost:8080"
