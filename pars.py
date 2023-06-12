import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os


server, wisual = False, True

DEBYG = True

if not DEBYG:
    server, wisual = False, False


def wait_by_class(class_name, driver):

    return WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))


def wait_by_Xpath(class_name, driver):

    return WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, class_name)))


def wb(prodId, lvl=0):

    options = Options()

    if server:
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

    if not wisual:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

    options.add_argument("--window-size=1200,2000")

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    if lvl > 3:
        return 0, 0
    try:
        driver.get(
            f'https://www.wildberries.ru/catalog/{prodId}/detail.aspx')

        driver.execute_script(
            "arguments[0].scrollIntoView();", wait_by_class('details-section', driver))
        reit = wait_by_class('user-opinion__rating-numb',
                             driver).text.replace('.', ',')
        col = re.findall(
            r'\d+', wait_by_class('user-opinion__text', driver).text)[0]

        return reit, col
    except Exception as e:
        if DEBYG:
            print(e)
        return wb(prodId, lvl+1)


def ozon(prodId, lvl=0):

    if lvl > 3:
        return 0, 0

    try:
        options = Options()

        if server:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')

        if not wisual:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')

        options.add_argument("--window-size=1600,1000")

        options.add_experimental_option("prefs", {"profiles.default_content_setting_values.notifications" : 2})
        options.add_argument("--allow-profiles-outside-user-dir")

        if server:
            options.add_argument(f"user-data-dir={os.getcwd()}/profiles/main")
        else:
            options.add_argument(f"user-data-dir={os.getcwd()}\\profiles\\main")
            
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

        driver.get(
            f'https://www.ozon.ru/product/{prodId}/reviews/')
        
        reit = wait_by_Xpath('//div[*]/div[*]/div/div[*]/div[*]/div/div[3]/div[4]/div[1]//span',
                             driver).text.split('/')[0].replace('.', ',')
        text = wait_by_Xpath('//*[@id="comments"]/div', driver).text

        return reit, text
    except Exception as e:
        if DEBYG:
            print(e)
        return ozon(prodId, lvl+1)

    # driver.execute_script(
    #     "arguments[0].scrollIntoView();", wait_by_class('details-section', driver))
    # reit = wait_by_class('user-opinion__rating-numb', driver).text
    # text = re.findall(
    #     r'\d+', wait_by_class('user-opinion__text', driver).text)[0]
    # return reit, text


if __name__ == '__main__':
    Id = '547464242'
    # print(wb(Id))
    # print(ozon(Id))
