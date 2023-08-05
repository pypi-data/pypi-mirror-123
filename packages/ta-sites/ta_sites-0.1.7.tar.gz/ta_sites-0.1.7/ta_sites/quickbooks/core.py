import logging
from ..basic.core import SitesCore
import os
import traceback


class QuickbooksCore(SitesCore):
    """
    Quickbooks object. Please Inheritance it.
    """
    def get_otp_code(self) -> str:
        """
        Please, modify this function in your code
        :return:
        """

        return ''

    def login_to_site(self) -> bool:
        self.is_site_available = False
        self.browser.close_browser()

        if self.temp_folder:
            if not os.path.exists(self.temp_folder):
                os.mkdir(self.temp_folder)
            self.browser.set_download_directory(self.temp_folder, True)

        for i in range(1, 4):
            try:
                self.browser.open_chrome_browser(self.url)
                self.browser.set_window_size(1920, 1080)
                self.browser.maximize_browser_window()

                self.wait_element('//input[@id="ius-signin-userId-input"]', timeout=30, is_need_screenshot=False)
                if self.does_element_displayed('//input[@id="ius-signin-userId-input"]'):
                    self.browser.input_text('//input[@id="ius-signin-userId-input"]', self.login)
                else:
                    self.browser.input_text('//input[@id="ius-userid"]', self.login)

                if self.does_element_displayed('//input[@id="ius-password"]'):
                    self.browser.input_text('//input[@id="ius-password"]', self.password)
                    self.browser.click_element_when_visible('//button[@id="ius-sign-in-submit-btn"]')
                else:
                    self.browser.click_element_when_visible('//button[@id="ius-sign-in-submit-btn"]')
                    self.wait_element('//input[@id="ius-sign-in-mfa-password-collection-current-password"]')
                    self.browser.input_text('//input[@id="ius-sign-in-mfa-password-collection-current-password"]', self.password)
                    self.browser.click_element_when_visible('//input[@id="ius-sign-in-mfa-password-collection-continue-btn"]')

                self.wait_element('//div[text()="Let\'s make sure you\'re you"]', timeout=10, is_need_screenshot=False)
                if self.does_element_displayed('//div[text()="Let\'s make sure you\'re you"]'):
                    self.browser.click_element_when_visible('//span[@id="ius-sublabel-mfa-email-otp"]')
                    self.browser.click_element_when_visible('//input[@id="ius-mfa-options-submit-btn"]')

                    self.wait_element('//input[@id="ius-mfa-confirm-code"]')
                    self.browser.input_text(
                        '//input[@id="ius-mfa-confirm-code"]',
                        self.get_otp_code()
                    )
                    self.browser.click_element_when_visible('//input[@id="ius-mfa-otp-submit-btn"]')
                self.wait_element('//div[@data-automation-id="cm_client_hub_business_name"]')
                if self.does_element_displayed('//div[@data-automation-id="cm_client_hub_business_name"]'):
                    self.base_url = self.get_base_url(self.browser.get_location())
                    self.is_site_available = True
                    return True
            except Exception as ex:
                logging.error(f'Login failed. Attempt {i}', 'ERROR')
                logging.error(str(ex))
                traceback.print_exc()
                self.browser.capture_page_screenshot(
                    os.path.join(self.output_folder, f'Login_failed_Attempt_{i}.png')
                )
                self.browser.close_browser()
        return False

    def go_to_client_page(self, client_name: str) -> None:
        """
        Navigate to client page

        :param client_name: Client name
        :return: None
        """
        self.click_bunch_of_elements([
            '//span[text()="GO TO QUICKBOOKS"]',
            f'//span[text()="{client_name}"]'
        ])
        self.wait_element(f'//div[contains(@class, "companyName") and text()="{client_name}"]')

    def open_add_invoice_page(self) -> None:
        """
        Open page 'Add invoice'
        """
        self.browser.go_to(f'{self.base_url}/app/homepage')

        self.click_bunch_of_elements([
            '//button[@data-id="global_create_button"]',
            '//a[@data-id="invoice"]'
        ])

    def open_invoices_page(self) -> None:
        """
        Check paid page
        """
        self.browser.go_to(f'{self.base_url}/app/homepage')
        self.click_bunch_of_elements([
            '//span[text()="Sales"]/..',
            '//a[text()="Invoices"]',
            '//th[@data-column-id="date"]',
            '//input[@aria-label="textFieldWrapper" and not(@data-automation-id)]',
            '//div[@value="paid"]',
            '//input[@aria-label="textFieldWrapper" and @data-automation-id="date-dropdown"]',
            '//div[@value="m:3"]',
        ])
        self.wait_element('//th[@data-column-id="date" and contains(@class, "sorted-desc")]', 5, False)
        if not self.browser.does_page_contain_element('//th[@data-column-id="date" and contains(@class, "sorted-desc")]'):
            self.browser.click_element_when_visible('//th[@data-column-id="date"]')
        self.wait_element('//div[@data-sale-status="PAID"]/../..', 15, False)
