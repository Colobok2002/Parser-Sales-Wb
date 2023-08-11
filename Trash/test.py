# import requests as r

# WB_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjhhZDcyNzQwLWExZTMtNGIwNy04ZDVkLTE1ZjRmZTRkZGExMyJ9.9_LcPW7E-JTqxl8g3VQiDCcs-5Q4-3DCHxqtq4XelDI"  # API KEY валдбересс

# print(
#     r.get(
#         f"https://suppliers-api.wildberries.ru/public/api/v1/info",
#         headers={"Authorization": WB_API},
#     ).json()
# )

from time import sleep
import keyboard


def emulate_keypress(key):
    keyboard.press_and_release(str(key))
    sleep(0.1)  # Пауза между нажатиями

code = "12341234"
for key in code:
    print(key)
    emulate_keypress(key)
