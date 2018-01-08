#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
import os
import subprocess
import re
import jira_config

debug = False

NAME = jira_config.NAME
PWD = jira_config.PWD

URL = 'https://jira.backdoro.com/secure/Dashboard.jspa'
BROWSE_URL = 'https://jira.backdoro.com/browse/'


def is_configured_properly():
    if NAME == 'your name' or NAME == '':
        return False
    else:
        return True


def create_driver():
    use_phantomjs = 1
    if use_phantomjs == 1:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 \
            (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        service_args = []
        service_args.append('--load-images=no')
        service_args.append('--disk-cache=yes')
        service_args.append('--ignore-ssl-errors=true')

        driver = webdriver.PhantomJS(
            executable_path='phantomjs',
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
    if not is_configured_properly:
        driver.quit()
        print("Please set your name and password before access jira. ~/.gitdull/jira_config.py")
        exit(-1)

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


def navigation(driver, bug_id):
    if debug:
        print("browse %s at " % bug_id, datetime.datetime.now())
    burl = BROWSE_URL + bug_id
    driver.get(burl)
    # driver.get('https://jira.backdoro.com/browse/%s' % bug_id)
    try:
        WebDriverWait(driver, 60, 0.5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="summary-val"]')))
    except TimeoutException:
        raise TimeoutException('Can not access %s' % burl)
    return driver


def browse(driver, bug_id):
    if debug:
        print("browse %s at " % bug_id, datetime.datetime.now())
    driver.get(BROWSE_URL + bug_id)
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
    navigation(dr, bid)
    tl = dr.find_element_by_xpath('//*[@id="summary-val"]').text
    dr.quit()
    return tl


def write_commit_info(bid, msg):
    dr = create_driver()
    login_jira(dr)
    navigation(dr, bid)
    comment = dr.find_element_by_id('comment-issue')
    comment.click()
    comment = dr.find_element_by_xpath("//textarea[@name='comment']")
    comment.clear()
    comment.send_keys(msg)
    dr.find_element_by_id('issue-comment-add-submit').click()
    time.sleep(2)
    dr.quit()
    return dr


def get_current_branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').readline().strip('\n')
    pass


def push_to_gerrit():
    br = get_current_branch()
    print("pushing %s to msm8909-la-3-0_amss_DORO_8035" % br)
    cmd = "git push origin " + br + ":refs/for/msm8909-la-3-0_amss_DORO_8035/" + br
    sp = subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          bufsize=-1)

    result = sp.communicate()
    stdo = result[0].decode('utf-8')
    stde = result[1].decode('utf-8')
    result = stdo + stde

    mt = re.search(r"remote: +(http://\S*) ", result)
    if mt is not None:
        result = mt.group(1)
    else:
        raise Exception('push fail')
    return result


def push_to_gerrit(remote_branch):
    br = get_current_branch()
    print("pushing %s to %s" % (br, remote_branch))
    cmd = "git push origin " + br + ":refs/for/" + remote_branch + "/" + br
    sp = subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          bufsize=-1)

    result = sp.communicate()
    stdo = result[0].decode('utf-8')
    stde = result[1].decode('utf-8')
    result = stdo + stde

    mt = re.search(r"remote: +(http://\S*) ", result)
    if mt is not None:
        result = mt.group(1)
    else:
        raise Exception('push fail')
    return result


if __name__ == '__main__':
    p = datetime.datetime.now()
    st = push_to_gerrit()
    print("Write commit info to jira...")

    print(st)
    dr = write_commit_info(get_current_branch(), "Fixed.\n" + st)
    print("DONE. ", datetime.datetime.now() - p)
