#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  4 12:39:02 2018

@author: Joseph Beaver

Add points to your co-op membership thing, the automated way!"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CoOp(object):
    """Object for manipulating bits of the Co-Operative website."""

    def __init__(self, headless: bool = True) -> None:
        sign_in_url = 'https://membership.coop.co.uk/sign-in'

        user_data_file = 'user_data.txt'

        with open(user_data_file) as f:
            sign_in_data = {}

            for line in f:
                key, value = line.strip().split(':')
                sign_in_data[key] = value

        chrome_options = Options()
        chrome_options.set_headless(headless)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.driver.get(sign_in_url)

        sign_in_title = self.driver.title
        print(f'At page: "{sign_in_title}".')

        try:
            print('Filling in login information.')
            for key, value in sign_in_data.items():
                input_element = self.driver.find_element_by_name('member-'+key)
                input_element.send_keys(value)
        except:
            print('Unable to sign in')
            self.exit_driver()
            raise SystemExit

        input_element.submit()
        print('Signed in!')

        try:
            WebDriverWait(self.driver,
                          15).until_not(EC.title_is(sign_in_title))
        except TimeoutError:
            print(f'Timeout exception - expected page title, "{sign_in_title}",\
                  could not be found.')
            self.exit_driver()
            raise SystemExit

        return None

    def add_receipt(self, *args) -> None:
        """Add a receipt."""

        args = [str(x) for x in args]

        transaction_keys = (
            'till-id',
            'store-id',
            'day-of-transaction',
            'month-of-transaction',
            'year-of-transaction',
            'transaction-id',
        )

        self.transaction_info = {}

        for i, arg in enumerate(args):
            self.transaction_info[transaction_keys[i]] = arg

        signed_in_title = self.driver.title
        print(f'At page: "{signed_in_title}".')

        link_text = 'Add a missed receipt'

        input_element = self.driver.find_element_by_link_text(link_text)

        print(f'Clicking link: "{link_text}".')
        input_element.click()

        try:
            WebDriverWait(self.driver,
                          15).until_not(EC.title_is(signed_in_title))
        except TimeoutError:
            print(f'Timeout exception - expected page title, "{signed_in_title}",\
                  could not be found.')

            return None

        receipt_add_title = self.driver.title
        print(f'At page: "{receipt_add_title}".')

        print('Filling in receipt information.')
        for key, value in self.transaction_info.items():
            input_element = self.driver.find_element_by_id(key)
            input_element.send_keys(value)

        print('Submitting receipt information.')
        input_element.submit()

        try:
            success_xpath = '//div[@class="message message-success"]'
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, success_xpath)
                )
            )
        finally:
            print(f'Timeout exception - expected xpath, "{success_xpath}", could not be found.')

            return None

        receipt_added_title = self.driver.title
        print(f'At page: "{receipt_added_title}".')

        return None

    def exit_driver(self) -> None:
        """Close the webdriver."""

        print('Exiting driver.')
        self.driver.close()


if __name__ == '__main__':
    headless, till_id, store_id, day, month, year, transaction_no\
            = sys.argv[1:]
    headless = bool(headless)
    coop = CoOp(headless)
    coop.add_receipt(till_id, store_id, day, month, year, transaction_no)
    coop.exit_driver()
