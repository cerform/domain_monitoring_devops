from selenium.webdriver.common.by import By
import time

def test_master_view(driver, base_url):
    driver.get(f"{base_url}/master")

    assert "Master" in driver.title

    table = driver.find_element(By.ID, "domains-table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    assert len(rows) > 0
