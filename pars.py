from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import requests as r
from datetime import datetime
from random import randint
from time import sleep


# CONSTS
# Где запушена программа на сервере или пк , отображать окна браузера или нет
server, wisual = False, False
PROFILE = "main"  # Профиль для браузера
wind = False  # Используется винда или linux
DEBYG = True  # Режем отладки
# PHONE = "9083059463"  # Номер телефона для авторизации на WB
PHONE = "9534499755"
WB_API = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNTEyMDQxNSwiaWQiOiI5ZjMyZTAxMS1lMGEzLTQ5ZTItYTFjMC0yMzE1ZDcxYjRiMTAiLCJpaWQiOjQ5NzI0NzA2LCJvaWQiOjEzNTE2LCJzIjoxMDczNzQyMzM0LCJzaWQiOiI2NzhkYjcwZS04ZGYzLTU4NWQtOWEzNi0yMDBlYjVlODc3YTkiLCJ1aWQiOjQ5NzI0NzA2fQ.ui3whOwCa1xzG74vF7RZfPZj-3H9V986Q5CIyWg05b4wH6a4oJ9XGoQSCEz3vuL71ynFve-XnxEotz9IWmXCJQ"  # API KEY валдбересс


def wait_by_class(class_name, driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )


def wait_by_Xpath(xpath, driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def wait_by_Id(id, driver):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))


def selekt_profile(name):
    options = webdriver.ChromeOptions()

    options.add_argument("--disable-extensions")

    if server:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")

    if not wisual:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

    options.add_argument("--allow-profiles-outside-user-dir")
    options.add_argument("--enable-profiles-shortcut-manager")

    if wind:
        options.add_argument(f"user-data-dir={os.getcwd()}\\profiles\\{name}")
    else:
        options.add_argument(f"user-data-dir={os.getcwd()}/profiles/{name}")

    options.add_argument("--profiles-directory=Default")

    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    return driver


def add_profile(name):
    print("[+] add profiles start")
    driver = selekt_profile(name)

    driver.get("https://www.wildberries.ru/security/login")

    wait_by_class("input-item", driver).send_keys(PHONE)

    wait_by_class("login__btn", driver).click()

    input("Введите Entr при успешной авторизации")

    print("[+] Profile create suksesful")

    return driver


def add_profile_server(name):
    print("[+] add profiles start")

    driver = selekt_profile(name)

    driver.get("https://www.wildberries.ru/security/login")

    wait_by_class("input-item", driver).send_keys(PHONE)

    wait_by_class("login__btn", driver).click()

    try:
        flag = True
        wait_by_Id("smsCaptchaCode", driver)

        while flag:
            driver.save_screenshot("smsCaptcha.png")
            code = input(
                "Captcha code (send + if Captcha succeeded send - if sreen bad?or cheek) - "
            )
            if code == "+":
                flag = False
            elif code == "-":
                continue
            else:
                wait_by_Id("smsCaptchaCode", driver).send_keys(code)
                sleep(5)
    except:
        None

    code = input("Введите код для авторизации - ")
    wait_by_class("input-item", driver)

    wait_by_class("sign-in-page", driver).click()
    driver.find_elements(By.CLASS_NAME, "input-item")[0].click()

    input("Введите Entr при успешной авторизации")

    print("[+] Profile create suksesful")

    return driver


def openWb():
    driver = selekt_profile(PROFILE)

    driver.get(f"https://www.wildberries.ru/")

    input("Нажмите для завершения")

    driver.close()


def chek_date(date, date_two):
    now = date_two

    date = datetime.strptime(date.split("T")[0], "%Y-%m-%d")

    if date.date() == now.date():
        return True

    return False


def get_prise_wb(prodId, lvl=0):
    if lvl >= 2:
        return {"nov": "", "old": "", "delt": ""}

    try:
        prise = {"nov": "", "old": "", "delt": ""}

        driver = selekt_profile(PROFILE)

        driver.get(f"https://www.wildberries.ru/catalog/{prodId}/detail.aspx")

        nov = (
            wait_by_class("price-block__final-price", driver)
            .get_attribute("textContent")
            .replace("₽", "")
            .replace(" ", "")
            .replace("\xa0", "")
        )
        old = (
            wait_by_class("price-block__old-price", driver)
            .get_attribute("textContent")
            .replace("₽", "")
            .replace(" ", "")
            .replace("\xa0", "")
        )

        prise["nov"] = nov
        prise["old"] = str(
            (int(nov) * 100) / round((int(nov) / int(old)) * 100, 0)
        ).split(".")[0]
        prise["delt"] = str(round(100 - (int(nov) / int(old)) * 100, 0)).split(".")[0]

        driver.close()
        if DEBYG:
            print(prise)
        return prise

    except Exception as e:
        if DEBYG:
            print(e)
        try:
            driver.close()
        except:
            None

        return get_prise_wb(prodId, lvl + 1)


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

    if lvl > 3:
        return "", "", {"5": "", "4": "", "3": "", "2": "", "1": ""}

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

        driver.get(f"https://www.ozon.ru/product/{prodId}/reviews/")

        wait_by_Xpath('//*[@id="comments"]/div', driver)

        driver.execute_script(f"window.scrollBy(0, {randint(200,300)});")

        reit = (
            wait_by_Xpath(
                "//div[*]/div[*]/div/div[*]/div[*]/div/div[3]/div[4]/div[1]//span",
                driver,
            )
            .text.split("/")[0]
            .replace(".", ",")
        )
        text = wait_by_Xpath('//*[@id="comments"]/div', driver).text

        reit_star = {"5": "", "4": "", "3": "", "2": "", "1": ""}

        for i in range(1, 6):
            reit_star[f"{abs(6-i)}"] = wait_by_Xpath(
                f"//div[@data-widget='webReviewProductScore']/div/div/div[2]/div[{i}]/div[3]",
                driver,
            ).text

        for i in reit_star:
            if reit_star[i] == 0 or reit_star[i] == "0":
                reit_star[i] = ""

        driver.close()

        return reit, text, reit_star

    except Exception as e:
        driver.close()

        if DEBYG:
            print(e)

        return new_ozon(prodId, lvl + 1)


def wb(prodId, lvl=0, date=datetime.now()):
    """new_wb парсинг с wb

    Функция через селениум получает данные о цене и спомошью API оплучает отзывы и рейтинг

    рейтинг:float ;
    колличество отзывов:int ;
    количетсво отзывов по звездам : list ('рейтинг':'колличество отзывов');
    цены : list ('nov текушаяя цена': 'значение','old старая цена': 'значение','delt скидка': 'значение' )

    Args:
        prodId (_type_): артикул wb
        lvl (int, optional): Уровень вложености . Defaults to 0.

    """

    if lvl > 7:
        return (
            "",
            "",
            {"5": "", "4": "", "3": "", "2": "", "1": ""},
        )

    try:
        response = r.get(
            f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/nmid?nmId={prodId}",
            headers={"Authorization": WB_API},
        )
        while response.status_code != 200:
            response = r.get(
                f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/nmid?nmId={prodId}",
                headers={"Authorization": WB_API},
            )

        reit, col = (
            response.json()["data"]["valuation"],
            response.json()["data"]["feedbacksCount"],
        )

        reit_star = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}

        response = r.get(
            f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/archive?skip=0&take=5000&nmId={prodId}&order=dateDesc",
            headers={"Authorization": WB_API},
        )

        while response.status_code != 200:
            response = r.get(
                f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks/archive?skip=0&take=5000&nmId={prodId}&order=dateDesc",
                headers={"Authorization": WB_API},
            )

        data = response.json()["data"]["feedbacks"]

        for i in data:
            if chek_date(i["createdDate"], date):
                reit_star[f"{i['productValuation']}"] += 1
        for i in reit_star:
            if reit_star[i] == 0:
                reit_star[i] = 0
        # if DEBYG:

        #     print(reit.replace(".", ","), col, reit_star)
        reit_star=dict(zip(["five", "four", "three", "two", "one"],reit_star.values()))
        return reit, col, reit_star
    except Exception as e:
        # if DEBYG:
        #     print(e)

        return wb(prodId, lvl + 1, date)


if __name__ == "__main__":
    Id = "242969350"
    # print(wb(Id))
    # print(ozon(Id))
    # wb_test(1)
    # print(new_ozon(Id))
    # print(new_wb('21358431'))
    add_profile(PROFILE)
    # print(wb('21358431'))
    # if server:
    # add_profile_server("test1")
    # else:
    openWb()

    # add_profile_server("test")
