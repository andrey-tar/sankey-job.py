import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def downloadSheet(fileKey, sheetName):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Lenovo/Desktop/PythonProjects/creds.json', scope)
    client = gspread.authorize(credentials)
    #### reading data in
    sheet = client.open_by_key(fileKey)  # file needs to be shared  with "client_email" from "credentials.json"
    sheet = sheet.worksheet(sheetName)
    data = sheet.get_all_records()
    data = pd.DataFrame.from_dict(data)
    print(f'downloading of {sheetName} successful')
    return data


def uploadToSheet(data,fileKey,sheetName):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Lenovo/Desktop/PythonProjects/creds.json', scope)
    client = gspread.authorize(credentials)
    workbook = client.open_by_key(fileKey)
    worksheetsRaw = workbook.worksheets()
    worksheets = [str(x).split('\'')[1] for x in worksheetsRaw]
    if np.logical_not('Sheet99' in worksheets):
        workbook.add_worksheet(title='Sheet99', rows=data.shape[0], cols=data.shape[1]) #add random sheet, so that 'Sheet1' can be cleaned if needed
    sheetPresenceMask = [x == sheetName for x in worksheets]
    if any(sheetPresenceMask):
        worksheet = workbook.worksheet(title=sheetName)
        worksheet.clear()
    else:
        worksheet = workbook.add_worksheet(title=sheetName, rows=data.shape[0], cols=data.shape[1])
    worksheetsRaw = workbook.worksheets()
    worksheets = [str(x).split('\'')[1] for x in worksheetsRaw]
    sheet99PresenceMask = [x == 'Sheet99' for x in worksheets]
    workbook.del_worksheet(np.array(worksheetsRaw)[sheet99PresenceMask][0])
    data = data.fillna('')
    data.replace(np.inf, 1, inplace=True)
    worksheet.update([data.columns.values.tolist()] + data.values.tolist())
    print('upload to sheet successful')
