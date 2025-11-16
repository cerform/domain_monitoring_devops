from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.bulk_upload_modal import BulkUploadModal
from pages.single_domain_modal import SingleDomainModal



class DashboardPage(BasePage):

    add_domain_button = (By.ID, "openAddDomain")
    bulk_upload_button = (By.ID, "openBulkUpload")

    def open_bulk_upload(self):
        self.click(self.bulk_upload_button)
        return BulkUploadModal(self.driver)

    def open_add_single_domain(self):
        self.click(self.add_domain_button)
        return SingleDomainModal(self.driver)
