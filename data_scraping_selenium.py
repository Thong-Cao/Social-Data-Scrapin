import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.firefox.options import Options

import time


import datetime
import time


import pandas as pd
from helium import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

url = 'https://www.instagram.com/highlandscoffeevietnam/'
#url = 'https://www.instagram.com/thecoffeehousevn/'
#url = 'https://www.instagram.com/starbucksvietnam/'
user = ''
pass_word = ''

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver.get(url)
set_driver(driver)
print('Starting to requests %s' %url)
wait = WebDriverWait(driver, 10)
time.sleep(3)

path_login_start = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/section/nav/div[2]/div/div/div[2]/div/div/div[2]/div[1]/a'
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path_login_start)))
driver.find_element(By.XPATH, path_login_start).click()
time.sleep(3)
path_login = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input'
path_pass = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input'
button = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]'
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path_login)))
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, path_pass)))

driver.find_element(By.XPATH, path_login).send_keys(user)
driver.find_element(By.XPATH, path_pass).send_keys(pass_word)
driver.find_element(By.XPATH, button).click()

time.sleep(5)
not_now_button = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'

driver.find_element(By.XPATH, not_now_button).click()

time.sleep(3)


# Click on first Post
p = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/div/div[1]/div[1]/a/div[1]'
driver.find_element(By.XPATH, p).click()


df = pd.DataFrame()
for i in range(700):
    time.sleep(2)

    try:
        xpath_post_text = '/html/body/div[{0}]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1'
        xpath_date = '/html/body/div[{0}]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/span/time'
        xpath_like = '/html/body/div[{0}]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span'
        xpath_next = '/html/body/div[{0}]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button'.format(str(i))
        text = driver.find_element(By.XPATH, xpath_post_text).text
        datetime_ = driver.find_element(By.XPATH, xpath_date).get_attribute('datetime')
        like = driver.find_element(By.XPATH, xpath_like).text

        driver.find_element(By.XPATH, xpath_next).click()
        if text != '':
            break
    except:
        continue
    print(text)
    lst = text.split('#')

    # Convert datetime just once to avoid repetition
    formatted_datetime = datetime.datetime.strptime(datetime_, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%d/%m/%Y')

    # Initialize the base record
    record = {
        'Post_ID': i,
        'text': lst[0] if lst else "",
        'datetime': formatted_datetime,
        'like': like,
        'hagtags1': "",
        'hagtags2': "",
        'hagtags3': "",
        'hagtags4': ""
    }

    # Update hashtags based on the length of lst
    if len(lst) >= 3:
        record['hagtags1'] = lst[2]
    if len(lst) >= 4:
        record['hagtags2'] = lst[3]
    if len(lst) >= 5:
        record['hagtags3'] = lst[4]
    if len(lst) > 5:
        record['hagtags4'] = lst[5:]  # This will store the remaining items as a list
    # Append the record to the dataframe
    df = df.append([record]) 
    print(i, end = "  ")
    print(df)


