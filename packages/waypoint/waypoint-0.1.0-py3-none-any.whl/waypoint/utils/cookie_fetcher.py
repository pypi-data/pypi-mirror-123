from urllib.parse import urlparse, parse_qs, unquote
from typing import Union

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager


class CookieFetcher:
    oauth_link = (
        "https://login.live.com/oauth20_authorize.srf?client_id=000000004C0BD2F1&scope=xbox.basic+xbox"
        ".offline_access&response_type=code&redirect_uri=https://www.halowaypoint.com/auth/callback&locale"
        "=en-us&display=touch&state=https%3a%2f%2fwww.halowaypoint.com%2fen-us%2fgames%2fhalo-the-master"
        "-chief-collection%2fxbox-one%2fgame-history%3fview%3dDataOnly"
    )
    oauth_dest = unquote(parse_qs(urlparse(oauth_link).query)["state"][0])
    webdriver_service = Service(ChromeDriverManager().install())
    webdriver_options = ChromeOptions()
    webdriver_options.headless = True

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.driver: Union[Chrome, None] = None
        self.wait: Union[WebDriverWait, None] = None
        self.get_driver()

    def get_driver(self, timeout: int = 5):
        self.cleanup()
        self.driver = Chrome(
            service=self.webdriver_service,
            options=self.webdriver_options,
        )
        self.wait = WebDriverWait(self.driver, timeout)

    def cleanup(self):
        if self.driver:
            self.driver.quit()

    def perform_auth(self) -> str:
        # Navigate to OAuth link
        self.driver.get(self.oauth_link)

        # Fill out username and click to next step
        username_el = self.driver.find_element(By.NAME, "loginfmt")
        username_el.send_keys(self.username)
        next_btn = self.driver.find_element(By.ID, "idSIButton9")
        next_btn.click()

        # Wait for sign in button to become clickable & fill out password & continue
        self.wait.until(ec.element_to_be_clickable((By.ID, "idSIButton9")))
        password_el = self.driver.find_element(By.NAME, "passwd")
        password_el.send_keys(self.password)
        signin_btn = self.driver.find_element(By.ID, "idSIButton9")
        signin_btn.click()

        # Wait until redirect has finished, then return Auth cookie
        self.wait.until(ec.url_to_be(self.oauth_dest))
        cookie = self.driver.get_cookie("Auth")
        if cookie:
            self.cleanup()
            return cookie["value"]

        # Loop if failure, this is common for this service
        self.get_driver()
        return self.perform_auth()
