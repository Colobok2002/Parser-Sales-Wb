from requests import post as p

from pars import DEBYG


def addPrise(dataPiche):
    URL = "https://data.riche.skin/app/v1.0/import_price/"
    TOKEN = "69a3d8da962b6f596a2244e3214dd142"

    # FC/22/FC/ACNE/50

    prods = []

    for prod in dataPiche:
        prods.append(
            {
                "marking": prod,
                "price": dataPiche[prod]["old"],
                "sale": dataPiche[prod]["delt"],
                "price_with_sale": dataPiche[prod]["new"],
            }
        )
    if DEBYG:
        print(len(prods))
        for i in prods:
            print(i)

    data = {"token": TOKEN, "items": prods}

    response = p(URL, json=data)

    print(response.text)
