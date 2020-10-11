"""
File:           telegram.py
Author:         Dibyaranjan Sathua
Created on:     10/10/20, 6:32 pm
"""
import os
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class SathuaLabCrawler:
    """ Crawl telegram using selenium """
    URL = "https://my.telegram.org/"
    CHROMEDRIVER_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../lib/chromedriver")
    )
    APP_NAME = "SathuaLabCrawler"
    APP_SHORT_NAME = "SathuaLabCrawler"
    APP_URL = "www.sathualab.com"
    APP_DESCRIPTION = "Telegram App created automatically by SathuaLab Crawler."

    def __init__(self, phone_no):
        self.phone_no = phone_no        # Phone number should be in international format
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        self.driver: Optional[webdriver.Chrome] = None
        self.app_api_id = None
        self.app_api_hash = None

    def __enter__(self):
        """ Context manager enter function """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Context manager exit function """
        if self.driver:
            self.driver.close()

    def crawl(self):
        self.driver = webdriver.Chrome(
            executable_path=self.CHROMEDRIVER_PATH,
            options=self.options
        )
        self.driver.implicitly_wait(5)
        self.driver.get(self.URL)
        time.sleep(1)
        self._send_phone_number()
        login_code = input("Enter your login code sent your Telegram app: ")
        login_code = login_code.strip()
        self._send_login_code(login_code)
        time.sleep(1)
        self._click_api_link()
        time.sleep(2)
        self._create_app()
        time.sleep(2)
        self._parse()

    def _send_phone_number(self):
        """ Send Phone number to the server to get the code on Telegram app """
        phone_no_field = self.driver.find_element_by_id("my_login_phone")
        phone_no_field.send_keys(self.phone_no)
        # Click the next button
        next_btn = self.driver.find_element_by_xpath('//button[text()="Next"]')
        next_btn.click()

    def _send_login_code(self, login_code):
        """ Send login code """
        login_code_field = self.driver.find_element_by_id("my_password")
        login_code_field.send_keys(login_code)
        # Click the SignIn button
        signin_btn = self.driver.find_element_by_xpath('//button[text()="Sign In"]')
        signin_btn.click()

    def _click_api_link(self):
        """ Click on API link """
        link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "API development tools"))
        )
        # link = self.driver.find_element_by_link_text("API development tools")
        link.click()
        time.sleep(5)

    def _create_app(self):
        """ Create a new App """
        time.sleep(3)
        # App is already created
        if self.driver.title == "App configuration":
            return None
        # app_title = self.driver.find_element_by_id("app_title")
        app_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app_title"))
        )
        app_title.send_keys(self.APP_NAME)

        app_shortname = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app_shortname"))
        )
        app_shortname.send_keys(self.APP_SHORT_NAME)

        # app_url = self.driver.find_element_by_id("app_url")
        app_url = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app_url"))
        )
        app_url.send_keys(self.APP_URL)

        # app_desc = self.driver.find_element_by_id("app_desc")
        app_desc = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app_desc"))
        )
        app_desc.send_keys(self.APP_DESCRIPTION)

        # save_btn = self.driver.find_element_by_id("app_save_btn")
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app_save_btn"))
        )
        save_btn.click()
        time.sleep(5)

    def _parse(self):
        """ Parse the page to get App Id and Hash """
        WebDriverWait(self.driver, 10).until(
            EC.title_is("App configuration")
        )
        form_group = self.driver.find_elements_by_css_selector("div.form-group")
        app_api_id_form = form_group.pop(0)
        self.app_api_id = app_api_id_form.find_element_by_css_selector("span").text
        app_api_hash_form = form_group.pop(0)
        self.app_api_hash = app_api_hash_form.find_element_by_css_selector("span").text
