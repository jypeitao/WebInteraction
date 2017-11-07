#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import datetime

URL = 'https://jira.backdoro.com/'
NAME = 'tao.pei@ck-telecom.com'
PWD = 'ckt123456'

print(datetime.datetime.now())
driver = webdriver.Chrome("/Users/peter/selenium_webdriver/chromedriver")
# driver = webdriver.PhantomJS()
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
time.sleep(20)
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
print(comment.is_selected())
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
