#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from userinfo import UserInfo

URL = UserInfo.URL
NAME = UserInfo.NAME
PWD = UserInfo.PWD
debug = False


def create_driver():
    HEADLESS = 1
    if HEADLESS == 1:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 \
            (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        service_args = []
        service_args.append('--load-images=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')

        driver = webdriver.PhantomJS( \
            executable_path='C:\\Users\\admin\\Desktop\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs',
            desired_capabilities=dcap, service_args=service_args)
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
        options.add_argument('headless')
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=options)
    return driver


def login_jira(driver):
    if debug:
        print("login ", datetime.datetime.now())
    driver.get(URL)
    try:
        user_name = WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.ID, "login-form-username"))
        )
        user_name.clear()
        user_name.send_keys(NAME)
    finally:
        pass

    pass_word = driver.find_element_by_id('login-form-password')
    pass_word.clear()
    pass_word.send_keys(PWD)

    submit = driver.find_element_by_id('login')
    submit.click()
    if debug:
        print("login submit ", datetime.datetime.now())
    try:
        WebDriverWait(driver, 20, 0.5).until(is_login_jira)
        if debug:
            print("Login succeed", datetime.datetime.now())
    finally:
        pass


def is_login_jira(driver):
    cook = driver.get_cookie("atlassian.xsrf.token")
    if (cook is not None) and (cook['value'].endswith("|lin")):
        return True
    else:
        return False


def browse(driver, bug_id):
    if debug:
        print("browse %s at " % bug_id, datetime.datetime.now())
    driver.get('https://jira.backdoro.com/browse/%s' % bug_id)
    try:
        WebDriverWait(driver, 60, 0.5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="summary-val"]')))
        sm = driver.find_element_by_xpath('//*[@id="summary-val"]')
        if debug:
            print("XPATH %s OK " % bug_id, datetime.datetime.now())
            sm = driver.find_element_by_xpath('//*[@id="summary-val"]')
            print(sm.text)
    finally:
        return sm.text


def get_title(bid):
    dr = create_driver()
    login_jira(dr)
    tl = browse(dr, bid)
    dr.quit()
    return tl

if __name__ == '__main__':
    p = datetime.datetime.now()
    title = get_title('BTTF-927')
    print(title)
#    dr = create_driver()
#    login_jira(dr)
#    browse(dr, 'MOTU-2154')
#    print(dr.title)
    print(datetime.datetime.now() - p)
#    dr.quit()



