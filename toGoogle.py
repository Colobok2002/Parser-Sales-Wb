import sys
from tqdm import tqdm
from google_tabels import GoogleTabelManager
from pars import ChromeDriverManager


class ParserManager:
    def __init__(self):
        """Init"""
        self.gtm = GoogleTabelManager()
        self.cdm = ChromeDriverManager()

    def updatePrise(self) -> None:
        prods = self.gtm.get_prods()

        result = {}
        for prod in tqdm(prods, desc="Рейтинг Wb", file=sys.stderr):
            result[prod] = {"name": "test", **self.cdm.get_prise_wb(url=prod)}

        self.gtm.update_google_sheet(result)


if __name__ == "__main__":
    pm = ParserManager()
    pm.updatePrise()
