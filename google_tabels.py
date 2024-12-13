import re

import gspread

TABLE_NAME = "prod_prise"  # Название самого эксель документа прям как на сайте
PRODS = "Продукты"  # Название листка с продуктами
PRISES = "Цены"  # Название листка с ценами


class GoogleTabelManager:
    def __init__(self) -> None:
        self.gc = gspread.service_account(filename="token.json")
        spreadsheet = self.gc.open(TABLE_NAME)
        self.wks_products = spreadsheet.worksheet(PRODS)
        self.wks_prices = spreadsheet.worksheet(PRISES)

    def get_product_price(url):
        return 4

    def get_prods(self) -> list[str]:
        """Получает все валидные ссылки на продукты из Google Sheets"""
        all_urls = self.wks_products.col_values(1)
        pattern = r"^https://www\.wildberries\.ru/catalog/\d+/detail\.aspx\??.*$"

        valid_urls = [url for url in all_urls if url and re.match(pattern, url)]

        return valid_urls

    def update_google_sheet(self, product_data: dict[str, dict[str, str]]) -> bool:
        """Основная функция для работы с Google Sheets и обновления данных о продуктах"""
        self.wks_prices.clear()

        # Заголовки столбцов
        headers = ["Ссылка", "Цена со скидкой", "Цена без скидки", "Скидка %"]

        self.wks_prices.update("A1:D1", [headers])
        data_to_update = []
        for _, (url, data) in enumerate(product_data.items(), start=1):
            row = [url, data.get("new", ""), data.get("old", ""), data.get("delt", "")]
            data_to_update.append(row)

        self.wks_prices.update(f"A2:D{len(data_to_update) + 1}", data_to_update)

        return True


if __name__ == "__main__":
    # Вызов функции
    gtm = GoogleTabelManager()

    prods = gtm.get_prods()

    result = {}
    for prod in prods:
        result[prod] = {"name": "test", "price": 1132.20}

    gtm.update_google_sheet(result)
