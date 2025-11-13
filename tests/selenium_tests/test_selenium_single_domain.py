from selenium.webdriver.common.by import By
import time


def test_single_domain_page(driver, base_url):
    driver.get(f"{base_url}/domains")

    assert "Domains" in driver.title

    first = driver.find_elements(By.CLASS_NAME, "domain-item")[0]
    domain_name = first.text
    first.click()

    time.sleep(1)

    body = driver.find_element(By.TAG_NAME, "body").text
    assert domain_name in body
