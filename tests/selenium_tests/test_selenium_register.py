from selenium.webdriver.common.by import By
import time
import uuid


def test_register_domain(driver, base_url):
    driver.get(f"{base_url}/register")

    assert "Register" in driver.title

    domain_name = f"test-{uuid.uuid4().hex[:6]}.com"
    domain_input = driver.find_element(By.ID, "domain")
    submit = driver.find_element(By.ID, "register-btn")

    domain_input.send_keys(domain_name)
    submit.click()

    time.sleep(1)

    # Проверяем появление записи
    body = driver.find_element(By.TAG_NAME, "body").text
    assert domain_name in body
