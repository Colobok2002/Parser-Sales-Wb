import requests
from datetime import datetime, timedelta

# from Trash.main import GoogleSheets, create_table
from pars import DEBYG, wb, get_prise_wb
import json
from addRicheSkin import addPrise
from apscheduler.schedulers.blocking import BlockingScheduler
from tqdm import tqdm
import time
import sys


def _requests(**kwargs):
    host = "http://127.0.0.1:8001"
    host = "https://data.riche.one"

    # api_url = "api/v1/"
    headers = {"HeaderApiKey":"Y2o2LxHtk1Rq4Ntj1kh7N1Ki86Fh25cgfFeRuu5z6t6JwWNQ7m"}
    api_url = "/"
    method = kwargs.get("method")
    url_zap = f"{host}{api_url}{method}"
    response = requests.get(url_zap, json=kwargs.get("data", False),headers=headers)

    if DEBYG:
        print(
            f"[{response.status_code}] {response.json() if response.status_code == 200 else 'Error'}"
        )
        print(f"[{response.status_code}]")

    return response.json()


def _requests_post(**kwargs):
    host = "http://127.0.0.1:8001"
    host = "https://data.riche.one"
    # api_url = "api/v1/"
    api_url = "/"
    headers = {"HeaderApiKey":"Y2o2LxHtk1Rq4Ntj1kh7N1Ki86Fh25cgfFeRuu5z6t6JwWNQ7m"}
    method = kwargs.get("method")
    url_zap = f"{host}{api_url}{method}"
    response = requests.post(url_zap, json=kwargs.get("data", False),headers=headers)

    if DEBYG:
        print(
            f"[{response.status_code}] {response.json() if response.status_code == 200 else 'Error'}"
        )

    return response.json()


# def addProdsSite():
#     table = "1UyxGOB1qr9LwFT5ARzA6My0_jkQbwXeI1ecb8qTxLv0"

#     apiGoogle = GoogleSheets("productsraiting-93d7111b4c98.json")
#     dataOzon = apiGoogle.GetData(table, "ozon")

#     if dataOzon["status"]:
#         dataOzon = dataOzon["data"]

#     data = []

#     for i in dataOzon:
#         dataKesh = {
#             "name": dataOzon[i]["Название"]["value"],
#             "art": dataOzon[i]["Внутрений арт"]["value"],
#             "wb": "",
#             "ozon": (
#                 dataOzon[i]["ozon"]["value"]
#                 if "ozon" in dataOzon[i]
#                 else dataOzon[i]["OZON"]["value"]
#             ),
#         }
#         data.append(dataKesh)
#     _requests(data=data, metod="addStatistecsProducts/")

#     dataWb = apiGoogle.GetData(table, "wb")

#     if dataWb["status"]:
#         dataWb = dataWb["data"]

#     data = []
#     for i in dataWb:
#         dataKesh = {
#             "name": dataWb[i]["Название"]["value"],
#             "art": dataWb[i]["Внутрений арт"]["value"],
#             "wb": (
#                 dataWb[i]["wb"]["value"]
#                 if "wb" in dataWb[i]
#                 else dataWb[i]["WB"]["value"]
#             ),
#             "ozon": "",
#         }
#         data.append(dataKesh)
#     _requests(data=data, metod="addStatistecsProducts/")

#     if 1 != 1:
#         create_table(apiGoogle)


def addWbOtchet(currentDate=None):
    data = _requests(metod="allProds/")["art"]
    if currentDate is None:
        date_now = datetime.now() - timedelta(days=1)
        date_date = datetime.strptime(date_now.date().strftime("%Y-%m-%d"), "%Y-%m-%d")
        date_str = date_now.date().strftime("%Y-%m-%d")
    else:
        date_date = datetime.strptime(currentDate, "%Y-%m-%d")
        date_str = currentDate
    response_data = []

    for i in tqdm(data, desc="Рейтинг Wb", file=sys.stderr):
        if DEBYG:
            print(i)
        if i["wb"] == None or "" == i["wb"] or "!" in i["wb"]:
            response_data.append(
                [i["art"], 0, 0, {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}]
            )
        else:
            reit, colvo_rev, reit_star = wb(i["wb"], date=date_date)
            response_data.append([i["art"], reit, colvo_rev, reit_star])
            if DEBYG:
                print([i["art"], reit, colvo_rev, reit_star])
    requestData = {"date": f"{date_str}", "market": "wb", "othet": response_data}

    _requests(
        metod="addStatsProds/",
        data=requestData,
    )


def addWbOtchetNew(currentDate=None):
    data = _requests(method="product/get_articles/")["data"]
    if currentDate is None:
        date_now = datetime.now() - timedelta(days=1)
        date_date = datetime.strptime(date_now.date().strftime("%Y-%m-%d"), "%Y-%m-%d")
        date_str = date_now.date().strftime("%d.%m.%Y")
    else:
        date_date = datetime.strptime(
            datetime.strptime(currentDate, "%Y-%m-%d").date().strftime("%Y-%m-%d"),
            "%Y-%m-%d",
        )
        date_str = (
            datetime.strptime(currentDate, "%Y-%m-%d").date().strftime("%d.%m.%Y")
        )
    response_data = []
    if DEBYG:
        print(date_str)
    for i in tqdm(data, desc="Рейтинг Wb", file=sys.stderr):
        if DEBYG:
            print(i)
        if i["wb"] == []:
            response_data.append(
                {
                    "art": i["art"],
                    "wb_art": "",
                    "rating": 0,
                    "total_otzv": 0,
                    "five": 0,
                    "four": 0,
                    "three": 0,
                    "two": 0,
                    "one": 0,
                }
            )
        else:
            for x in i["wb"]:
                if "\t" in x:
                    response_data.append(
                        {
                            "art": i["art"],
                            "wb_art": x,
                            "rating": 0,
                            "total_otzv": 0,
                            "five": 0,
                            "four": 0,
                            "three": 0,
                            "two": 0,
                            "one": 0,
                        }
                    )
                else:
                    reit, colvo_rev, reit_star = wb(x, date=date_date)
                    response_data.append(
                        {
                            "art": i["art"],
                            "wb_art": x,
                            "rating": reit,
                            "total_otzv": colvo_rev,
                            **reit_star,
                        }
                    )
    requestData = {"date": f"{date_str}", "market": "wb", "otchet": response_data}

    _requests_post(
        method="analitycs/add_rating_from_mp/",
        data=requestData,
    )


def updatePrise():
    responseData = _requests(method="chem/get_products_wb_art/")

    prods = responseData.get("data", False)

    if prods:
        dataPise = {}
        for prod in tqdm(prods, desc="Цены", file=sys.stderr):
            if DEBYG:
                print(prod)
            prise = get_prise_wb(prod)
            if prise != {"new": "", "old": "", "delt": ""}:
                dataPise[prods[prod]] = {
                    "old": prise["old"],
                    "delt": prise["delt"],
                    "new": prise["new"],
                }
        addPrise(dataPise)


def calculate_price(*product_prices):
    return round(sum(product_prices) * 0.95, 2)  # Применяем скидку 5%


def updatePriseNabor():
    import requests
    import xml.etree.ElementTree as ET

    url = "https://data.riche.skin/rcrm/"
    response = requests.get(url)

    if response.status_code == 200:
        xml_content = response.content
    else:
        print("Ошибка при получении данных:", response.status_code)
        return False

    root = ET.fromstring(xml_content).find("shop").find("offers")
    kits = {}

    responseData = _requests(method="chem/get_products_wb_art/")
    prods = responseData.get("data", {}).values()

    for offer in root.findall("offer"):
        product_type = offer.find('param[@name="Тип продукта"]').text
        if product_type == "Комплект":
            set_contents = [
                set_content.text
                for set_content in offer.findall('param[@name="Состав комплекта"]')
            ]
            set_prices = []
            for xmlId in set_contents:
                for item in root.findall(f'.//offer[xmlId="{xmlId}"]'):
                    product_price_elem = item.find("price")
                    if product_price_elem is not None:
                        product_price = float(product_price_elem.text)
                        set_prices.append(product_price)

            new_price = calculate_price(*set_prices)

            # price = offer.find("purchasePrice").text

            if not offer.find('param[@name="Артикул"]').text in prods:
                kits[offer.find('param[@name="Артикул"]').text] = {
                    "old": new_price, 
                    "delt": 0,
                    "new": new_price,
                }

    addPrise(kits)

if __name__ == "__main__":
    updatePrise()
    # updatePriseNabor()
    # updatePrise()
    # updatePrise()
    # if 1 != 1:
    #     # addProdsSite()
    #     None
    # if DEBYG:
    #     addWbOtchetNew()
    #     if True:
    #         date = [
    #             "2023-12-03",
    #             "2023-12-04",
    #             "2023-12-05",
    #             "2023-12-06",
    #             "2023-12-07",
    #         ]
    #         # for i in date:
    #         # addWbOtchet(i)

    #     # addWbOtchet()
    #     # updatePrise()
