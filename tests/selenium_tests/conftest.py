import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Global Fixtures

@pytest.fixture
def driver():
    # For headless mode:
    # options = Options()
    # options.add_argument("--headless=new")
    
    # Installing Browser:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # For headless mode:
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Optional:
    driver.maximize_window()
    driver.implicitly_wait(5)
    # Yield\Return the driver to the test
    yield driver 
    # Quit when done
    driver.quit()   

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8080")


