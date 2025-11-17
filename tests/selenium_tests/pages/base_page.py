from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    PATH = "/"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver=self.driver, timeout=5)
        self.base_url = base_url
    # Actions:
    def load(self):
        self.driver.get(f"{self.base_url}{self.PATH}")
    
    def get_title(self):
        return self.driver.title

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def wait_for(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator=locator))

    def type(self, locator, text):
        self.wait_for(locator=locator).send_keys(text)
    
    def get_text(self, locator):
        return self.wait_for(locator=locator).text

    def is_visible(self, locator):
        try:
            self.wait_for(locator=locator)
            return True
        except Exception as e:
            return False