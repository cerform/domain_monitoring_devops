from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def create_linux_driver():
    options = Options()

    # use the one that actually exists on your system:
    options.binary_location = "/usr/bin/chromium-browser"  # or "/usr/bin/chromium"

    # headless etc.
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # again: match what `which chromedriver` gave you
    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)


if __name__ == "__main__":
    driver = create_linux_driver()
    driver.get("https://google.com")
    print(driver.title)
    driver.quit()
