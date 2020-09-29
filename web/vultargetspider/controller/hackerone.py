#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: hackerone.py
@time: 2020/4/22 11:25
@desc:
'''


import re
import time
import requests
import traceback
from core.chromeheadless import ChromeDriver
from utils.log import logger
from LSpider.settings import HACKERONE_USERNAME, HACKERONE_PASSWORD

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class HackeroneSpider:
    """
    hackerone spider main core
    """
    def __init__(self):

        self.url = 'https://hackerone.com/'
        self.chromeclass = ChromeDriver()

        self.login_url = "https://hackerone.com/users/sign_in"
        self.username = HACKERONE_USERNAME
        self.password = HACKERONE_PASSWORD

    def spider(self, appname):
        url = self.url + appname

        # login
        self.login()
        time.sleep(5)

        code, content = self.chromeclass.get_resp(url, isclick=False)
        time.sleep(5)

        result = self.html_parse()

        return result

    def html_parse(self):
        result_list = []

        td_list = self.chromeclass.driver.find_elements_by_xpath("//td[@class='daisy-table__cell table__row--align-top break-word']")

        for td in td_list:

            try:
                domain = td.find_element_by_tag_name("strong").text.strip()

                url_list = td.find_element_by_tag_name('p').text
                for url in url_list.split("\n"):
                    if url.startswith("/"):
                        u = "http://" + domain + url.strip()

                        # replace {} () <>
                        u = re.sub(r'[({<][^)}>]*[)}>]', '1', u)

                        result_list.append(u.replace("*.", ""))

            except:
                logger.warnning("[Hackerone spider][parse] url data parse error. {}".format(traceback.format_exc()))
                continue

        return result_list

    def dealcookie(self, cookie):
        cookies = {}

        for data in cookie.split(';'):
            if data:
                key = data.split('=')[0]
                value = data.split('=')[1]

                if key and value:
                    cookies[key] = value

        return cookies

    def login(self):

        self.chromeclass.get_resp(self.login_url, isclick=False)
        self.chromeclass.driver.refresh()

        user_elem = self.chromeclass.driver.find_element_by_name("user[email]")
        user_elem.send_keys(self.username)

        pass_elem = self.chromeclass.driver.find_element_by_name("user[password]")
        pass_elem.send_keys(self.password)

        submit_elem = self.chromeclass.driver.find_element_by_name("commit")
        submit_elem.click()

        return True


if __name__ == "__main__":

    h = HackeroneSpider()
    h.spider('opera')
