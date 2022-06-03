from pprint import pprint
from datetime import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

now = datetime.now()

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'credentials.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1AC2tPzF8UdVhfgNVgjJYxdNI-Gm7gPTHFZ1G6VNQR5s'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Пример чтения файла
def get_from_spreadsheets(spreadsheet_id):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:E31',
        majorDimension='ROWS'
    ).execute()
    return values

# Пример записи в файл
def load_to_spreadsheets(spreadsheet_id,new_value):
    day = int(now.strftime('%d'))+1
    service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A1:C1",
             "majorDimension": "COLUMNS",
             "values": [["Дата"],["Расходы"], ["Доходы"]]},
            {"range": f"A{day}:C{day}",
             "majorDimension": "COLUMNS",
             "values": [["=СЕГОДНЯ()"], [new_value[1]], [new_value[2]]]}
        ]
        }
    ).execute()
