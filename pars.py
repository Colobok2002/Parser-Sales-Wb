from random import randint
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

# CONSTS
server, wisual = False, False # Где запушена программа на сервере или пк , отображать окна браузера или нет
ROFILE = "main" # Профиль для браузера
wind = True # Используется винда или linux
DEBYG = False # Режем отладки
PHONE = "9196602851" # Номер телефона для авторизации на WB

if not DEBYG:
    server, wisual = False, True
    

def wait_by_class(class_name, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))


def wait_by_Xpath(xpath, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_by_Id(id, driver):

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))

def add_profile(name):

    print("[+] add profiles start")
    options = webdriver.ChromeOptions()

    if server:
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

    if not wisual:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profiles-shortcut-manager')

    if not wind:
        options.add_argument(f"user-data-dir={os.getcwd()}/profiles/{name}")
    else:
        options.add_argument(f"user-data-dir={os.getcwd()}\\profiles\\{name}")

    options.add_argument('--profiles-directory=Default')

    driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

   
    driver.get('https://www.wildberries.ru/security/login')
    
    wait_by_class('input-item',driver).send_keys(PHONE)
    
    wait_by_class('login__btn',driver).click()
    
    input("Введите Entr при успешной авторизации")
    
    print("[+] Profile create suksesful")

    return driver


def selekt_profile(name):

    options = webdriver.ChromeOptions()

    if server:
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

    if not wisual:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

    options.add_argument('--allow-profiles-outside-user-dir')
    options.add_argument('--enable-profiles-shortcut-manager')

    if not wind:
        options.add_argument(f"user-data-dir={os.getcwd()}/profiles/{name}")
    else:
        options.add_argument(f"user-data-dir={os.getcwd()}\\profiles\\{name}")

    options.add_argument('--profiles-directory=Default')

    driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

    return driver


def new_wb(prodId, lvl=0):
    """new_wb парсинг с wb

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

    # driver = webdriver.Chrome(service=ChromeService(
    #     ChromeDriverManager().install()), options=options)
    
    driver = selekt_profile(ROFILE)

    if lvl > 7:
        
        return 0, 0 ,{"5":0,"4":0,"3":0,"2":0,"1":0},{'nov':0,'old':0,'delt':0}
    
    try:
        
        driver.get(
            f'https://www.wildberries.ru/catalog/{prodId}/feedbacks')

        
        reit = wait_by_class('rating-product__all-rating', driver).text.replace('.', ',')
        
        col = wait_by_class('rating-product__review',driver).find_element(By.TAG_NAME,"span").text.replace(' ', '')
        
        reit_star = {"5":0,"4":0,"3":0,"2":0,"1":0}
        try:
            for i in driver.find_elements(By.CLASS_NAME,'feedback-percent'):
                reit_star[i.find_element(By.CLASS_NAME,'feedback-percent__star').text] = str(round((int(col)*int(i.find_element(By.CLASS_NAME,'feedback-percent__count').text.replace('%','')))/100,0)).split('.')[0]
        except:
            None

        
        prise = {'nov':0,'old':0,'delt':0}
        try:
            driver.get(f'https://www.wildberries.ru/catalog/{prodId}/detail.aspx')
            nov = wait_by_class('price-block__final-price',driver).text.replace('₽','').replace(' ','')
            old = wait_by_class('price-block__old-price',driver).text.replace('₽','').replace(' ','')
            prise['nov'] = nov
            prise['old'] = old
            prise['delt'] = str(round((int(prise['nov'])/int(prise['old']))*100,0)).split('.')[0]
        except:
            None
        
        return reit, col , reit_star ,prise
    
    except Exception as e:
        
        driver.close()
        
        if DEBYG:
            
            print(e)
            
        return new_wb(prodId, lvl+1)

def new_ozon(prodId, lvl=0):
    """new_ozon данные с Ozon

    рейтинг:float ; 
    колличество отзывов:int ; 
    количетсво отзывов по звездам : list ('рейтинг':'колличество отзывов'); 

    Args:
        prodId (_type_): артикул ozon
        lvl (int, optional): уровень вложености. Defaults to 0.

    Returns:
        _type_: _description_
    """
    
    if lvl > 7:
        return 0, 0 ,{"5":0,"4":0,"3":0,"2":0,"1":0}

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
        reit_star = {"5":0,"4":0,"3":0,"2":0,"1":0}
        
        for i in range(1,6):
            reit_star[f"{abs(6-i)}"] = wait_by_Xpath(f"//div[@data-widget='webReviewProductScore']/div/div/div[2]/div[{i}]/div[3]",driver).text
            
        
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
    # print(new_ozon(Id))
    # print(new_wb('21358431'))
    add_profile(ROFILE)
 