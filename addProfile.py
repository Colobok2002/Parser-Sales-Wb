"""
:mod:`addProfile` -- Создать профиль для показания цен в кошельке
===================================
.. moduleauthor:: ilya Barinov <i-barinov@it-serv.ru>
"""

from pars import ChromeDriverManager


if __name__ == "__main__":
    cdm = ChromeDriverManager()
    cdm.add_profile()
