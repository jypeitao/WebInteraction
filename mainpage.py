from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

from userinfo import UserInfo

URL = UserInfo.URL
NAME = UserInfo.NAME
PWD = UserInfo.PWD

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)


class CreateDriver:
    @staticmethod
    def get_driver():
        head_less = 0
        if head_less == 1:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 \
                (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
            driver = webdriver.PhantomJS( \
                executable_path='C:\\Users\\admin\\Desktop\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs',
                desired_capabilities=dcap)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument(
                'user-agent="Mozilla/5.0 \
                (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"')
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2
                }
            }
            # options.add_experimental_option('prefs', prefs)
            # driver = webdriver.Chrome(chrome_options=options)
            driver = webdriver.Chrome("/Users/peter/selenium_webdriver/chromedriver", chrome_options=options)
        return driver


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def get(self, url):
        self.driver.get(url)


class JiraLogin:
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        user_name = self.driver.find_element_by_id('login-form-username')
        user_name.clear()
        user_name.send_keys(NAME)

        password = self.driver.find_element_by_id('login-form-password')
        password.clear()
        password.send_keys(PWD)

        submit = self.driver.find_element_by_id('login')
        submit.click()


if __name__ == "__main__":
    logger.info("it's main")
    p = MainPage(CreateDriver.get_driver())
    # p.get('https://www.baidu.com/')
    p.get(URL)
    JiraLogin(p.driver).login()

