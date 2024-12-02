from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as ChromeDriverManagerBase

# CONSTS

wisual = True  # Отображать окна браузера или нет
PROFILE = "main"  # Профиль для браузера
DEBYG = False  # Режем отладки
PHONE = "..."


class ChromeDriverManager:
    def wait_by_class(self, class_name, driver):
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )

    def wait_by_Xpath(self, xpath: str, driver):
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def wait_by_Id(self, id, driver):
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))

    def selekt_profile(self, name):
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-extensions")

        if not wisual:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

        options.add_argument("--allow-profiles-outside-user-dir")
        options.add_argument("--enable-profiles-shortcut-manager")

        profile_path = Path(Path.cwd()) / "profiles" / name
        options.add_argument(f"user-data-dir={profile_path}")

        options.add_argument("--profiles-directory=Default")

        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManagerBase().install()), options=options
        )

        return driver

    def add_profile(self, name=PROFILE):
        print("[+] add profiles start")
        driver = self.selekt_profile(name)

        driver.get("https://www.wildberries.ru/security/login")

        self.wait_by_class("input-item", driver).send_keys(PHONE)

        self.wait_by_class("login__btn", driver).click()

        input("Введите Entr при успешной авторизации")

        print("[+] Profile create suksesful")

        return driver

    def add_profile_server(self, name):
        print("[+] add profiles start")

        driver = self.selekt_profile(name)

        driver.get("https://www.wildberries.ru/security/login")

        self.wait_by_class("input-item", driver).send_keys(PHONE)

        self.wait_by_class("login__btn", driver).click()

        try:
            flag = True
            self.wait_by_Id("smsCaptchaCode", driver)

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
                    self.wait_by_Id("smsCaptchaCode", driver).send_keys(code)
                    sleep(5)
        except:
            None

        code = input("Введите код для авторизации - ")
        self.wait_by_class("input-item", driver)

        self.wait_by_class("sign-in-page", driver).click()
        driver.find_elements(By.CLASS_NAME, "input-item")[0].click()

        input("Введите Entr при успешной авторизации")

        print("[+] Profile create suksesful")

        return driver

    def get_prise_wb(self, prod_id=None, url=None, lvl=0):
        if lvl >= 2:
            return {"new": "", "old": "", "delt": ""}

        try:
            prise = {"new": "", "old": "", "delt": ""}

            driver = self.selekt_profile(PROFILE)
            if prod_id:
                driver.get(f"https://www.wildberries.ru/catalog/{prod_id}/detail.aspx")
            elif url:
                driver.get(url)
            else:
                raise ValueError("Не передан продукт")

            new = (
                self.wait_by_class("price-block__final-price", driver)
                .get_attribute("textContent")
                .replace("₽", "")
                .rplace(" ", "")
                .replace("\xa0", "")
            )
            old = (
                self.wait_by_class("price-block__old-price", driver)
                .get_attribute("textContent")
                .replace("₽", "")
                .replace(" ", "")
                .replace("\xa0", "")
            )

            prise["new"] = new

            prise["old"] = str((int(new) * 100) / round((int(new) / int(old)) * 100, 0)).split(".")[
                0
            ]

            prise["delt"] = str(round(100 - (int(new) / int(old)) * 100, 0)).split(".")[0]

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

            return self.get_prise_wb(prod_id, url, lvl + 1)
