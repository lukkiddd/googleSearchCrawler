from google import search
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
sht2 = gc.open('RefinnDoc')
worksheet = sht2.get_worksheet(0)

list_name = []
list = []
for i in search('refinn', stop=100, lang="th"):
    name = i.split('//')[1].replace('www.','').split('.')[0]
    if name not in list_name and name not in ['facebook','th-th']:
        data = req.get(i)
        soup = BeautifulSoup(data.text)
        text = soup.title.text if soup.title else 'none'
        list_name.append(name)
        list.append([name, text, i, datetime.datetime.now()])

df = pd.DataFrame(list)
df.columns = ['name', 'title', 'link', 'time']
j = 1
for col in df.columns:
    worksheet.update_cell(1, j, col)
    j = j+1
for index, row in df.iterrows():
    k=1
    for col in df.columns:
        worksheet.update_cell(index+2, k, row[col])
        k = k+1
