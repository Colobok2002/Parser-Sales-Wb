from requests import post as p


def addPrise(art, price, sale, price_with_sale):
    print(art, price, sale, price_with_sale)
    URL = "https://data.riche.skin/app/v1.0/import_price/"
    TOKEN = "69a3d8da962b6f596a2244e3214dd142"

    # FC/22/FC/ACNE/50
    prods = [
        {
            "marking": art,
            "price": price,
            "sale": sale,
            "price_with_sale": price_with_sale,
        }
    ]

    # 449.00

    data = {"token": TOKEN, "items": prods}

    response = p(URL, json=data)

    print(response.text)
