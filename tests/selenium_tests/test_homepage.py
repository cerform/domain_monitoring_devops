# tests/selenium_tests/test_homepage.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_open_python_org():
    """Открываем python.org и проверяем заголовок"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.python.org/")
    title = driver.title
    driver.quit()

    assert "Python" in title
