from typing import Callable

from selenium import webdriver


class CookieThief:
    def __init__(
        self,
        login_url: str,
        do_login: Callable[[webdriver.Chrome], None],
    ):
        self.do_login = do_login
        self.login_url = login_url

    @staticmethod
    def __get_driver() -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        # disable loading images
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument(
            "--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1"
        )

        options.headless = True

        return webdriver.Chrome(options=options)

    def __get_cookies(self):
        print("[CookieThief] Getting Chrome webdriver")
        driver = CookieThief.__get_driver()
        print("[CookieThief] Navigating to Login page")
        driver.get(self.login_url)

        print("[CookieThief] Logging in...")
        self.do_login(driver)

        print("[CookieThief] Stealing cookies...")
        cookies = driver.get_cookies()
        driver.close()

        result = {}
        for cookie in cookies:
            result[cookie["name"]] = cookie["value"]

        return result

    def __call__(self) -> dict:
        return self.__get_cookies()

