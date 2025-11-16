from pages.dashboard_page import DashboardPage
from utils.domain_factory import generate_domain_file


def test_bulk_upload_ui(logged_in):

    browser = logged_in
    dashboard = DashboardPage(browser)

    # Step 1 - open modal
    modal = dashboard.open_bulk_upload()

    # Step 2 - generate domain file
    file_path, domains = generate_domain_file("selenium_tests/tests")

    # Step 3 - upload file through modal
    dashboard = modal.upload_file(file_path)

    # Step 4 - verify uploaded domains appear
    page = browser.page_source.lower()
    for d in domains:
        assert d in page, f"{d} is missing from dashboard"

    print("[OK] Bulk upload UI test passed.")
