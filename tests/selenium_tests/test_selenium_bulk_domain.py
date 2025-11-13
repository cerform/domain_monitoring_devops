from selenium.webdriver.common.by import By
import time
import uuid


def test_bulk_add(driver, base_url):
    driver.get(f"{base_url}/bulk")

    assert "Bulk" in driver.title

    textarea = driver.find_element(By.ID, "domains-textarea")
    submit = driver.find_element(By.ID, "bulk-btn")

    dom1 = f"bulk-{uuid.uuid4().hex[:6]}.com"
    dom2 = f"bulk-{uuid.uuid4().hex[:6]}.net"

    textarea.send_keys(f"{dom1}\n{dom2}")
    submit.click()

    time.sleep(1)

    page = driver.find_element(By.TAG_NAME, "body").text

    assert dom1 in page
    assert dom2 in page
