#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import datetime

URL = 'https://jira.backdoro.com/'
NAME = 'tao.pei@ck-telecom.com'
PWD = 'ckt123456'

HEADLESS = 1
if HEADLESS == 1:
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
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.Chrome()
# driver = webdriver.Chrome("/Users/peter/selenium_webdriver/chromedriver")
driver.get(URL)

print(datetime.datetime.now())
# driver.implicitly_wait(100)
userName = driver.find_element_by_id('login-form-username')
userName.clear()
userName.send_keys(NAME)

passWord = driver.find_element_by_id('login-form-password')
passWord.clear()
passWord.send_keys(PWD)

submit = driver.find_element_by_id('login')
submit.click()

# Login in
BUG_ID = 'BTTF-405'

print("login...")
time.sleep(10)
print("already login")
driver.get('https://jira.backdoro.com/browse/%s' % BUG_ID)

print("show bug")
comment = driver.find_element_by_id('comment-issue')
comment.click()
print("comment click")
print(datetime.datetime.now())
# issue-comment-add-submit
comment = driver.find_element_by_xpath("//textarea[@name='comment']")
comment.clear()
comment.send_keys("this is a test")
print(datetime.datetime.now())
print("this is a test")
driver.find_element_by_id('issue-comment-add-submit').click()
print("this is a test2")

print(datetime.datetime.now())
# go quit
time.sleep(30)
# driver.close()
driver.quit()
