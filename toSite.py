import requests
from datetime import datetime, timedelta
from Trash.main import GoogleSheets, create_table
from pars import DEBYG, wb, get_prise_wb
import json
from addRicheSkin import addPrise
from apscheduler.schedulers.blocking import BlockingScheduler
from tqdm import tqdm
import time
import sys


def _requests(**kwargs):
    # host = "http://127.0.0.1:8000/"
    host = "https://app.riche.one/"
    api_url = "api/v1/"

    metod = kwargs.get("metod")

    url_zap = f"{host}{api_url}{metod}"

    response = requests.post(url_zap, json=kwargs.get("data", False))

    if DEBYG:
        print(
            f"[{response.status_code}] {response.json() if response.status_code == 200 else 'Error'}"
        )

    return response.json()


def addProdsSite():
    table = "1UyxGOB1qr9LwFT5ARzA6My0_jkQbwXeI1ecb8qTxLv0"

    apiGoogle = GoogleSheets("productsraiting-93d7111b4c98.json")
    dataOzon = apiGoogle.GetData(table, "ozon")

    if dataOzon["status"]:
        dataOzon = dataOzon["data"]

    data = []

    for i in dataOzon:
        dataKesh = {
            "name": dataOzon[i]["Название"]["value"],
            "art": dataOzon[i]["Внутрений арт"]["value"],
            "wb": "",
            "ozon": dataOzon[i]["ozon"]["value"]
            if "ozon" in dataOzon[i]
            else dataOzon[i]["OZON"]["value"],
        }
        data.append(dataKesh)
    _requests(data=data, metod="addStatistecsProducts/")

    dataWb = apiGoogle.GetData(table, "wb")

    if dataWb["status"]:
        dataWb = dataWb["data"]

    data = []
    for i in dataWb:
        dataKesh = {
            "name": dataWb[i]["Название"]["value"],
            "art": dataWb[i]["Внутрений арт"]["value"],
            "wb": dataWb[i]["wb"]["value"]
            if "wb" in dataWb[i]
            else dataWb[i]["WB"]["value"],
            "ozon": "",
        }
        data.append(dataKesh)
    _requests(data=data, metod="addStatistecsProducts/")

    if 1 != 1:
        create_table(apiGoogle)


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
        if "" == i["wb"] or "!" in i["wb"] or i["wb"] == None:
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


def updatePrise():
    responseData = _requests(metod="selektPriseProds/")
    prods = responseData.get("data", False)[0:10]

    if prods:
        dataPise = {}
        for prod in tqdm(prods, desc="Цены", file=sys.stderr):
            prise = get_prise_wb(prod["wb"])
            if prise != {"nov": "", "old": "", "delt": ""}:
                dataPise[prod["art"]] = {
                    "old": prise["old"],
                    "delt": prise["delt"],
                    "nov": prise["nov"],
                }

        print(dataPise)
        addPrise(dataPise)


if __name__ == "__main__":
    if 1 != 1:
        addProdsSite()
    if DEBYG:
        # addWbOtchet()
        if True:
            date = [
                "2023-08-04",
                "2023-08-05",
                "2023-08-06",
                "2023-08-07",
            ]
            for i in date:
                addWbOtchet(i)

        addWbOtchet()
        # updatePrise()
