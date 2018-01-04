#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thurs Jan  4 12:39:02 2018

@author: Joseph Beaver

Add points to your co-op membership thing, the automated way!"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sign_in_url = 'https://membership.coop.co.uk/sign-in'

user_data_file = 'user_data.txt'

with open(user_data_file) as f:
    sign_in_data = {}

    for line in f:
        key, value = line.strip().split(':')
        sign_in_data[key] = value

transaction_keys = (
    'till-id',
    'store-id',
    'day-of-transaction',
    'month-of-transaction',
    'year-of-transaction',
    'transaction-id',
)

transaction_info = {}

for i, arg in enumerate(sys.argv[1:]):
    transaction_info[transaction_keys[i]] = arg

chrome_options = Options()
chrome_options.set_headless(True)

# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.get(sign_in_url)

sign_in_title = driver.title
print(f'At page: "{sign_in_title}".')

print('Filling in login information.')
for key in sign_in_data.keys():
    input_element = driver.find_element_by_name('member-'+key)
    input_element.send_keys(sign_in_data[key])

input_element.submit()
print('Signed in!')

WebDriverWait(driver, 15).until_not(EC.title_is(sign_in_title))

signed_in_title = driver.title
print(f'At page: "{signed_in_title}".')

link_text = 'Add a missed receipt'

input_element = driver.find_element_by_link_text(link_text)

print(f'Clicking link: "{link_text}".')
input_element.click()

WebDriverWait(driver, 15).until_not(EC.title_is(signed_in_title))

receipt_add_title = driver.title
print(f'At page: "{receipt_add_title}".')

print('Filling in receipt information.')
for key in transaction_info.keys():
    input_element = driver.find_element_by_id(key)
    input_element.send_keys(transaction_info[key])

print('Submitting receipt information.')
input_element.submit()

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@class="message message-success"]')
    )
)

receipt_added_title = driver.title
print(f'At page: "{receipt_added_title}".')

print('Exiting driver.')
driver.close()
