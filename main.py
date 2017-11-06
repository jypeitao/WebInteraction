#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
import time

URL = 'https://jira.backdoro.com/'
NAME = 'tao.pei@ck-telecom.com'
PWD = 'ckt123456'

driver = webdriver.Chrome("/Users/peter/selenium_webdriver/chromedriver")
driver.get(URL)

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

time.sleep(20)
driver.get('https://jira.backdoro.com/browse/%s' % BUG_ID)

comment = driver.find_element_by_id('comment-issue')
comment.click()
# issue-comment-add-submit

# go quit
time.sleep(10)
# driver.close()
driver.quit()
