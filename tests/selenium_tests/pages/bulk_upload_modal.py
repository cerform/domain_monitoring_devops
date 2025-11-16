import os
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage



class BulkUploadModal(BasePage):

    file_input = (By.CSS_SELECTOR, "#bulkUploadForm input[type='file']")
    form = (By.ID, "bulkUploadForm")

    def upload_file(self, file_path):
        self.driver.find_element(*self.file_input).send_keys(file_path)

        form_el = self.driver.find_element(*self.form)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('submit', { bubbles: true }));",
            form_el
        )
        return DashboardPage(self.driver)
