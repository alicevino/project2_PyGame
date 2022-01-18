"""
Получение данных с котировками выбранных компаний
за определенный период времени.

На данный момент реализовано получение данных фиксированных компаний
за фиксированный отрезок времени.

Данные можно получить либо с Yahoo Finance, либо прочитать из
csv-файлов уже скаченные данные, что достаточно для игры.
"""

import csv

data_tsm = []
data_cvx = []
data_abbv = []
data_sony = []

"""
import yfinance as yf

# Получение котировок с Yahoo Finance
for c in yf.download('TSM', '2021-06-10', '2021-12-10')['Adj Close']:
    data_tsm.append(int(c))

for c in yf.download('CVX', '2021-06-10', '2021-12-10')['Adj Close']:
    data_cvx.append(int(c))

for c in yf.download('ABBV', '2021-06-10', '2021-12-10')['Adj Close']:
    data_abbv.append(int(c))

for c in yf.download('SONY', '2021-06-10', '2021-12-10')['Adj Close']:
    data_sony.append(int(c))

with open('tsm.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_tsm)
with open('cvx.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_cvx)
with open('abbv.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_abbv)
with open('sony.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(data_sony)
"""

# Чтение котировок из файлов
with open('data/tsm.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_tsm.extend(map(int, row))
with open('data/cvx.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_cvx.extend(map(int, row))
with open('data/abbv.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_abbv.extend(map(int, row))
with open('data/sony.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_sony.extend(map(int, row))



