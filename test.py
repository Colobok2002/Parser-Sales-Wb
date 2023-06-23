from requests import post as p

URL = "https://data.riche.skin/app/v1.0/import_price/"
TOKEN = "69a3d8da962b6f596a2244e3214dd142"


prods = [{"marking":
          "FC/45/EP/PMEP/100",
          "price": 499,
          "sale": 10,
          "price_with_sale": 400}]

# 449.00

data = {
    'token': TOKEN,
    "items": prods
}

response = p(URL,json=data)

print(response.text)
