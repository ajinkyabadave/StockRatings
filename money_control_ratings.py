
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread
import requests
import sqlite3 as sl
import datetime

con = sl.connect('my-test.db')
c = con.cursor()  
stocks_list = []

# 1000
# 3000 == 4000

c.execute('''SELECT * FROM stocks limit 10''')

rows = c.fetchall()


def get_data(row):
    code = row[0].split('/')[-1]
    name = row[0].split('/')[-2]
    url = row[0]
    print(row + " "+ datetime.datetime.now())
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')
    if soup.find('div', {'class': 'escnt'}) is not None and soup.find('div', {'class': 'escnt'}).find('div') is not None:
        rating = soup.find('div', {'class': 'escnt'}).find('div').text.split('%')[0]
    else:
        rating = ""    
    stocks_list.append({'stock_code': code, 'url': row[0], 'name': name, 'rating': rating})



for row in rows:
    get_data(row)
# commetning for testing parallel api calls

# c.execute('''CREATE TABLE IF NOT EXISTS money_control_ratings
#     (stock_code varchar[50], url varchar[1000], name varchar[1000], rating int);''')

for stock in stocks_list:
    # c.execute("INSERT INTO money_control_ratings VALUES (?,?,?,?)", (stock['stock_code'],stock['url'],stock['name'],stock['rating']))
   

    print((stock['stock_code'],stock['url'],stock['name'],stock['rating']))


con.commit();
con.close();

