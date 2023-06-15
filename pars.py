from random import randint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
import re
import os


server, wisual = False, False

DEBYG = True

if not DEBYG:
    server, wisual = False, False


def wait_by_class(class_name, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))


def wait_by_Xpath(xpath, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_by_Id(id, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))

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
        
        driver.close()
        
        if DEBYG:
            
            print(e)
            
        return wb(prodId, lvl+1)


def new_test(prodId, lvl=0):
    """new_test парсинг с wb

    Функция через селениум получает данные и взврашает 
    
    рейтинг:float ; 
    колличество отзывов:int ; 
    количетсво отзывов по звездам : list ('рейтинг':'колличество отзывов'); 
    цены : list ('nov текушаяя цена': 'значение','old старая цена': 'значение','delt скидка': 'значение' )

    Args:
        prodId (_type_): артикул wb
        lvl (int, optional): Уровень вложености . Defaults to 0.
        
    """
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

    if lvl > 15:
        
        return 0, 0
    
    try:
        
        driver.get(
            f'https://www.wildberries.ru/catalog/83511998/feedbacks')

        
        reit = wait_by_class('rating-product__all-rating', driver).text
        
        col = wait_by_class('rating-product__review',driver).find_element(By.TAG_NAME,"span").text.replace(' ', '')
        
        reit_star = {}
        for i in driver.find_elements(By.CLASS_NAME,'feedback-percent'):
            reit_star[i.find_element(By.CLASS_NAME,'feedback-percent__star').text] = str(round((int(col)*int(i.find_element(By.CLASS_NAME,'feedback-percent__count').text.replace('%','')))/100,0)).split('.')[0]

        
        prise = {}
        
        prise['nov'] = wait_by_class('product-line__price-now',driver).get_attribute("innerHTML")
        prise['old'] = wait_by_class('product-line__price-old',driver).text
        match = re.search(r'(\d+)\s*(&nbsp;)?₽', prise['nov'])
        prise['nov'] = match.group(1)
        match = re.search(r'(\d+(?: \d+)*)\s*₽', prise['old'])
        prise['old'] = match.group(1).replace(' ','')
    
        prise['delt'] = str(round((int(prise['nov'])/int(prise['old']))*100,0)).split('.')[0]
        
        return reit, col , reit_star ,prise
    
    except Exception as e:
        
        driver.close()
        
        if DEBYG:
            
            print(e)
            
        return new_test(prodId, lvl+1)


def ozon(prodId, lvl=0):

    if lvl > 15:
        return 0, 0

    try:
        options = Options()
        # options.add_argument('--headless=new')
        
        if server:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')

        if not wisual:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')

        options.add_argument("--window-size=1600,1000")

        # options.add_experimental_option("prefs", {"profiles.default_content_setting_values.notifications" : 2})
        # options.add_argument("--allow-profiles-outside-user-dir")

        # if server:
        #     options.add_argument(f"user-data-dir={os.getcwd()}/profiles/main")
        # else:
        #     options.add_argument(f"user-data-dir={os.getcwd()}\\profiles\\main")
            
        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

        driver.get(
            f'https://www.ozon.ru/product/{prodId}/reviews/')
        
        reit = wait_by_Xpath('//div[*]/div[*]/div/div[*]/div[*]/div/div[3]/div[4]/div[1]//span',
                             driver).text.split('/')[0].replace('.', ',')
        text = wait_by_Xpath('//*[@id="comments"]/div', driver).text

        return reit, text
    except Exception as e:
        driver.close()
        if DEBYG:
            print(e)
        return ozon(prodId, lvl+1)

    # driver.execute_script(
    #     "arguments[0].scrollIntoView();", wait_by_class('details-section', driver))
    # reit = wait_by_class('user-opinion__rating-numb', driver).text
    # text = re.findall(
    #     r'\d+', wait_by_class('user-opinion__text', driver).text)[0]
    # return reit, text

def new_ozon(prodId, lvl=0):
    
    if lvl > 15:
        return 0, 0

    try:
        options = FOptions()
        
        if server:
            options.headless = True
            options.set_preference("gfx.webrender.enabled", False)
            options.set_preference("layers.acceleration.disabled", True)
            
        if not wisual:
            options.headless = True
            options.set_preference("gfx.webrender.enabled", False)
            options.set_preference("layers.acceleration.disabled", True)

        driver_path = GeckoDriverManager().install()

        service = FirefoxService(executable_path=driver_path)

        driver = webdriver.Firefox(service=service, options=options)
        
        driver.get(
            f'https://www.ozon.ru/product/{prodId}/reviews/')
        
        wait_by_Xpath('//*[@id="comments"]/div', driver)

        driver.execute_script(f"window.scrollBy(0, {randint(200,300)});")
        
        reit = wait_by_Xpath('//div[*]/div[*]/div/div[*]/div[*]/div/div[3]/div[4]/div[1]//span',
                             driver).text.split('/')[0].replace('.', ',')
        text = wait_by_Xpath('//*[@id="comments"]/div', driver).text
        reit_star = {}
        
        for i in range(1,6):
            reit_star[abs(6-i)] = wait_by_Xpath(f"//div[@data-widget='webReviewProductScore']/div/div/div[2]/div[{i}]/div[3]",driver).text

        driver.close()
        
        return reit, text , reit_star
    
    except Exception as e:
        
        driver.close()
        
        if DEBYG:
            
            print(e)
            
        return new_ozon(prodId, lvl+1)
    

if __name__ == '__main__':
    Id = '242969350'
    # print(wb(Id))
    # print(ozon(Id))
    # wb_test(1)
    print(new_ozon(Id))