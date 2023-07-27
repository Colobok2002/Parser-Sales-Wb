import requests
from datetime import datetime, timedelta
from main import GoogleSheets, create_table
from pars import new_ozon, DEBYG, wb
import json
from addRicheSkin import addPrise
from apscheduler.schedulers.blocking import BlockingScheduler
from tqdm import tqdm
import time


def _requests(**kwargs):
    # host = "http://127.0.0.1:8000/"
    host = "http://app.riche.one/"
    api_url = "api/v1/"

    metod = kwargs.get("metod")

    url_zap = f"{host}{api_url}{metod}"

    response = requests.post(url_zap, json=kwargs.get("data", False))

    # print(
    #     f"[{response.status_code}] {response.json() if response.status_code == 200 else 'Error'}"
    # )

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


def addWbOtchet():
    data = _requests(metod="allProds/")["art"]
    date_now = datetime.now() - timedelta(days=1)
    date_date = datetime.strptime(date_now.date().strftime("%Y-%m-%d"), "%Y-%m-%d")
    date_str = date_now.date().strftime("%Y-%m-%d")
    response_data = []
    dataPise = {}
    for i in tqdm(data):
        if DEBYG:
            print(i)
        if "" == i["wb"] or "!" in i["wb"]:
            response_data.append(
                [i["art"], 0, 0, {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}]
            )
        else:
            reit, colvo_rev, reit_star, prisi = wb(i["wb"], date=date_date)
            if DEBYG:
                print(prisi)
            if prisi != {"nov": "", "old": "", "delt": ""}:
                dataPise[i["art"]] = {
                    "old": prisi["old"],
                    "delt": prisi["delt"],
                    "nov": prisi["nov"],
                }
            response_data.append([i["art"], reit, colvo_rev, reit_star, prisi])

    requestData = {"date": f"{date_str}", "market": "wb", "othet": response_data}
    _requests(
        metod="addStatsProds/",
        data=requestData,
    )
    addPrise(dataPise)


if __name__ == "__main__":
    if 1 != 1:
        addProdsSite()
    if DEBYG:
        addWbOtchet()

    else:
        while True:
            print("[+] Start")
            now = datetime.now()
            target_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

            if now >= target_time:
                addWbOtchet()
                tomorrow = now + timedelta(days=1)
                target_time = tomorrow.replace(
                    hour=16, minute=0, second=0, microsecond=0
                )
                print("[+] Finish")

            time_to_wait = (target_time - now).total_seconds()
            time.sleep(time_to_wait)
