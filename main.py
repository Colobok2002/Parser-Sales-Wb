import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from pars import wb,ozon , DEBYG
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

class GoogleSheets:

    def __init__(self, json_keu) -> None:

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keu,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        self.httpAuth = credentials.authorize(httplib2.Http())
        self.driveService = apiclient.discovery.build(
            'drive', 'v3', http=self.httpAuth)
        self.service = apiclient.discovery.build(
            'sheets', 'v4', http=self.httpAuth)

    def AddServiceAccount(self, tableId: str, emailAddress: str, riole: str = 'writer') -> dict:
        """AddServiceAccount Дать доступ к аккаунту

        Дать доступ к аккаунту на таблицу 

        Args:
            tableId (_type_): Id таблицы к которой нужно предоставить доступ
            gmailAddress (_type_): Адрес которому предоставляется доступ
            riole (str, optional): Роль которая дается . Defaults to 'writer'. По умолчанию чтение и запись

        Returns:
            dict: Статус выполнения и если есть ошибка, возвращается строку с ошибкой
        """

        try:
            self.driveService.permissions().create(
                fileId=tableId,
                body={'type': 'user', 'role': riole,
                      'emailAddress': emailAddress},
                fields='id'
            ).execute()
            return {'status': True}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def AddTable(self, name: str = "Table", properties: dict = {'sheetType': 'GRID', 'sheetId': 0, 'title': 'Первый лист', 'gridProperties': {'rowCount': 0, 'columnCount': 0}}) -> dict:
        """AddTable Добавить таблицу

        Создает таблицу с переданными парраметрами

        Args:
            name (str, optional): Названеи таблицы. Defaults to "Table".
            properties (_type_, optional): параметры создания. Defaults to {'sheetType': 'GRID', 'sheetId': 0, 'title': 'Первый лист'}.

        Returns:
            dict: _description_ {'status': True, 'spreadsheet': spreadsheet['spreadsheetId']}
        """
        try:
            spreadsheet = self.service.spreadsheets().create(body={
                'properties': {'title': name, 'locale': 'ru_RU'},
                'sheets': [{'properties': properties}]
            }).execute()

            return {'status': True, 'spreadsheet': spreadsheet['spreadsheetId']}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def AddList(self, spreadsheetId: str, name: str) -> dict:
        """AddList добавить лист 

        Добавляет лист в таблицу

        Args:
            spreadsheetId (str): id таблицы
            name (str): Названеи листа.

        Returns:
            dict: _description_
        """
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheetId,
                body={
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": name,
                                }
                            }
                        }
                    ]
                }).execute()
            return {'status': True}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def SelectSheet(self, spreadsheetId: str) -> dict:
        """SelectSheet Id листов таблицы

        Получает и возврашает все id листов в таблице

        Args:
            spreadsheetId (str): _description_

        Returns:
            dict: _description_
        """
        try:
            data = {}
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheetId).execute()
            sheetList = spreadsheet.get('sheets')
            for sheet in sheetList:
                data[sheet['properties']['title']
                     ] = sheet['properties']['sheetId']

            return {'status': True, 'data': data}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def addColumn(self, spreadsheetId: str, name: str, colvo_col: int = 4) -> dict:
        """addColumn Добавть колонки 

        Функции добаления колонок в таблицу

        Args:
            spreadsheetId (str): Название таблицы
            name (str): Название колонки
            colvo_col (int, optional): Сколько столбцов добавть. Defaults to 4.

        Returns:
            _type_: _description_
        """
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheetId).execute()
            sheets = spreadsheet['sheets']
            sheet = next(
                (s for s in sheets if s['properties']['title'] == name), None)
            sheet_properties = sheet['properties']
            grid_properties = sheet_properties['gridProperties']

            grid_properties['columnCount'] += colvo_col

            update_request = {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': sheet_properties['sheetId'],
                        'gridProperties': grid_properties,
                    },
                    'fields': 'gridProperties.columnCount',
                },
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheetId,
                body={'requests': [update_request]},
            ).execute()
            return {'status': True}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def GetData(self, spreadsheetId: str, nameTab: str, start_str: int = 2) -> dict:
        """GetData Получить данные из таблицы

        Args:
            spreadsheetId (str): Таблица
            nameTab (str): Название страницы
            start_str (int, optional): Строка с которой стоит считывать данные. Defaults to 2.

        Returns:
            dict: { id строки : {col_name: {value: value, column: column}} }
        """
        try:
            sheet = self.service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                             range=nameTab,
                                                             ).execute()
            values = sheet.get('values')
            data = {}

            for row_index, row in enumerate(values[start_str:]):
                row_data = {}
                if row != []:
                    for col_index, value in enumerate(row):
                        try:
                            if values[start_str][col_index] != "":
                                col_name = values[1][col_index]
                                row_data[col_name] = {
                                    'value': value, "column": col_index}
                        except:
                            continue
                    data[row_index + start_str + 1] = row_data
            return {'status': True, 'data': data}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def addData(self, spreadsheetId: str, sheet_name: str, yash: str, data: dict) -> dict:
        """addData Добавть данные в таблицу

        Args:
            spreadsheetId (str): Таблица
            sheet_name (str): Название страницы
            yash (str): Ячейка
            data (dict): Данные для добавления в таблицу формата  [[],[]]  где первый уровнь запись в столбик а втрой запись в строку

        Returns:
            dict: _description_
        """
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheetId,
                range=f'{sheet_name}!{yash}',
                valueInputOption='USER_ENTERED',
                body={'values': data}
            ).execute()

            return {'status': True, }
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}

    def number_to_column(self, num: int) -> dict:
        """number_to_column Буква ячейки из числа

        Args:
            num (int): Номер колонки

        Returns:
            dict: status  Буквенное обозначение колонки | Ошибка
        """
        try:
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            result = ''
            while num > 0:
                remainder = (num - 1) % 26
                result = alphabet[remainder] + result
                num = (num - 1) // 26
            return {'status': True, 'data': result}
        except Exception as e:
            return {'status': False, 'error': str(e)}

    def merge_cells(self, spreadsheetId: str, sheet_name: str, start_range: int, end_range: int, rov_start: int = 0, rov_fin: int = 1) -> dict:
        """merge_cells обеденение ячеек

        Args:
            spreadsheetId (str): Таблица
            sheet_name (str): Название страницы
            start_range (int): Начальный столбец  
            end_range (int): Конченый столбец  
            rov_start (int): Начальная строка
            rov_fin (int): Кончена строка

        Returns:
            dict: {'status': True | False}
        """
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheetId).execute()
            sheets = spreadsheet['sheets']
            sheet = next(
                (s for s in sheets if s['properties']['title'] == sheet_name), None)

            merge_request = {
                'mergeCells': {
                    'range': {
                        'sheetId': sheet['properties']['sheetId'],
                        'startRowIndex': rov_start,
                        'endRowIndex': rov_fin,
                        'startColumnIndex': start_range,
                        'endColumnIndex': end_range
                    },
                    'mergeType': 'MERGE_ALL'

                }
            }

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheetId,
                body={'requests': [merge_request]}
            ).execute()
            return {'status': True}
        except apiclient.errors.HttpError as e:
            return {'status': False, 'error': str(e)}


def add_data_wb(table,date) -> None:
    """add_data_wb Данные с WB

    Получает и записывает даннные с WB и записывает в таблицу
    """
    
    name_shhet = 'wb'
    apiGoogle.addColumn(table,name_shhet)
    data = apiGoogle.GetData(table, name_shhet)

    if data['status']:
        data = data['data']

    data_data = [['Рейтинг', 'Разница_р', 'Отзывов', 'Разница_о']]

    col = apiGoogle.number_to_column(
        data[next(iter(data))]['Рейтинг']['column']+5)

    if col['status']:
        col = col['data']

    apiGoogle.addData(table, name_shhet, f"{col}1", [
        [date]])

    col = f"{col}{next(iter(data))-1}"

    apiGoogle.merge_cells(table, name_shhet, data[next(iter(
        data))]['Рейтинг']['column']+4, data[next(iter(data))]['Рейтинг']['column']+8)

    for i in data:
        if DEBYG:
            print(i)
        if data[i]['WB']['value'] == "" or "!" in data[i]['WB']['value']:
            reit , colvo_rev =  0 , 0
        else:
            reit , colvo_rev =  wb(data[i]['WB']['value'])

        col_start = apiGoogle.number_to_column(
            data[i]['Рейтинг']['column']+5)
        if col_start:
            col_start = col_start['data']
        col_fin = apiGoogle.number_to_column(
            data[i]['Рейтинг']['column']+1)
        if col_fin:
            col_fin = col_fin['data']
        form1 = f"={col_start}{i}-{col_fin}{i}"

        col_start = apiGoogle.number_to_column(
            data[i]['Отзывов']['column']+5)
        if col_start:
            col_start = col_start['data']
        col_fin = apiGoogle.number_to_column(
            data[i]['Отзывов']['column']+1)
        if col_fin:
            col_fin = col_fin['data']
        form2 = f"={col_start}{i}-{col_fin}{i}"

        data_data.append([reit, form1, colvo_rev, form2])

    apiGoogle.addData(table, name_shhet, col, data_data)

def add_data_ozon(table,date) -> None:
    """add_data_wb Данные с Ozon

    Получает и записывает даннные с Ozon и записывает в таблицу
    """


    name_shhet = 'ozon'
    
    apiGoogle.addColumn(table,name_shhet)

    data = apiGoogle.GetData(table, name_shhet)

    if data['status']:
        data = data['data']

    data_data = [['Рейтинг', 'Разница_р', 'Отзывов', 'Разница_о']]

    col = apiGoogle.number_to_column(
        data[next(iter(data))]['Рейтинг']['column']+5)

    if col['status']:
        col = col['data']

    apiGoogle.addData(table, name_shhet, f"{col}1", [
        [date]])

    col = f"{col}{next(iter(data))-1}"

    apiGoogle.merge_cells(table, name_shhet, data[next(iter(
        data))]['Рейтинг']['column']+4, data[next(iter(data))]['Рейтинг']['column']+8)

    for i in data:
        if DEBYG:
            print(i)
        if data[i]['OZON']['value'] == "" or "!" in data[i]['OZON']['value']:
            reit , colvo_rev =  0 , 0
        else:
            reit , colvo_rev =  ozon(data[i]['OZON']['value'])

        col_start = apiGoogle.number_to_column(
            data[i]['Рейтинг']['column']+5)
        if col_start:
            col_start = col_start['data']
        col_fin = apiGoogle.number_to_column(
            data[i]['Рейтинг']['column']+1)
        if col_fin:
            col_fin = col_fin['data']
        form1 = f"={col_start}{i}-{col_fin}{i}"

        col_start = apiGoogle.number_to_column(
            data[i]['Отзывов']['column']+5)
        if col_start:
            col_start = col_start['data']
        col_fin = apiGoogle.number_to_column(
            data[i]['Отзывов']['column']+1)
        if col_fin:
            col_fin = col_fin['data']
        form2 = f"={col_start}{i}-{col_fin}{i}"

        data_data.append([reit, form1, colvo_rev, form2])

    apiGoogle.addData(table, name_shhet, col, data_data)



def main() -> None:
    table = '1yU_reTudQhR0ggF-6ZhVucY771kw-udYbvKveq6sGuE'
    date = datetime.now().strftime('%d.%m.%y')
    print(f"Программа запущена в 23:55 по МСК {date}")
    
    
    # add_data_wb(table,date)
    add_data_ozon(table,date)
    print('[+] Finished')

if __name__ == '__main__':
    
    
    apiGoogle = GoogleSheets('productsraiting-93d7111b4c98.json')

    def create_table():

        table = apiGoogle.AddTable(name="Статистика маркетплейсов", properties = {'sheetType': 'GRID', 'sheetId': 0, 'title': 'wb', 'gridProperties': {'rowCount': 0, 'columnCount': 0}})['spreadsheet']

        apiGoogle.AddServiceAccount(table, emailAddress="wotwotwot65@gmail.com")

        print('https://docs.google.com/spreadsheets/d/' + table)

        apiGoogle.AddList(table, name='ozon')

        return table

    if 1 != 1:
        create_table()
    
    if DEBYG:
        main()

    else:
    
        print('[+] Start')
        # print(datetime.now())
        scheduler = BlockingScheduler()

        scheduler.add_job(main, 'cron', hour=23, minute=55)

        # scheduler.add_job(main, 'cron', hour=18, minute=44)
        scheduler.start()