import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.selenium_tests.pages.dashboard_page import DashboardPage
from tests.selenium_tests.utils.domain_factory import generate_domain_file

THIS_DIR = os.path.dirname(__file__)


def test_bulk_upload_ui(logged_in):

    browser = logged_in
    dashboard = DashboardPage(browser)
    
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "greeting"))
    )

    # Step 1 - open modal
    modal = dashboard.open_bulk_upload()

    # Step 2 - generate domain file
    file_path, domains = generate_domain_file(THIS_DIR)

    # Step 3 - upload file through modal
    dashboard = modal.upload_file(file_path)

    # Step 4 - wait for dashboard to be active again
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "openAddDomain"))
    )

    # Step 5 - validate domains appear
    WebDriverWait(browser, 10).until(
        lambda d: all(domain in d.page_source.lower() for domain in domains)
    )

    print("[OK] Bulk upload UI test passed.")

    # CLEANUP
    if os.path.exists(file_path):
        os.remove(file_path)
