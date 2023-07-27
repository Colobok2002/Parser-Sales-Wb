import requests
import json

url = "https://www.ozon.ru/api/composer-api.bx/widget/json/v2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Content-Type": "application/json",
    "x-o3-app-name": "dweb_client",
    "x-o3-app-version": "release_24-6-2023_915fc08f",
    "Alt-Used": "www.ozon.ru"
}

data = {
    "asyncData": "eyJ1cmwiOiIvY29udGV4dC9kZXRhaWwvaWQvMTQ5NjY0NDEwLz9sYXlvdXRfY29udGFpbmVyPXBkcFJldmlld3MmbGF5b3V0X3BhZ2VfaW5kZXg9MiZzaD1ycnpGd21UUllnJnN0YXJ0X3BhZ2VfaWQ9ZDcyZjRiMDhiMzJiODhmNTlkYWY5MTU1NzI0ZTk5M2YmdGFiPXJldmlld3MiLCJjaSI6eyJuYW1lIjoid2ViUmV2aWV3UHJvZHVjdFNjb3JlIiwidmVydGljYWwiOiJycFByb2R1Y3QiLCJwYXJhbXMiOlt7Im5hbWUiOiJ0aXRsZSIsInRleHQiOiLQntCx0YnQuNC5INGA0LXQudGC0LjQvdCzIn0seyJuYW1lIjoiYW5jaG9yVXJsIn1dLCJpZCI6MzEzMTgwMiwidmVyc2lvbiI6MiwibGF5b3V0SUQiOjEwMzYxfX0="
}

response = requests.post(url, headers=headers, json=data)
response_data = response.text

print(response_data)
