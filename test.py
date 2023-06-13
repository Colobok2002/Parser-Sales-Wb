from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
# Установка пути к драйверу Gecko WebDriver
driver_path = GeckoDriverManager().install()

# Создание экземпляра сервиса Firefox
service = FirefoxService(executable_path=driver_path)

# Создание экземпляра драйвера Firefox с использованием сервиса
driver = webdriver.Firefox(service=service)

driver.get('https://www.ozon.ru/product/547464242/reviews/')


sleep(999)
driver.quit()