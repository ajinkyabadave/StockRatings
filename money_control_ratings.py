from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread
import requests
import sqlite3 as sl
import datetime
import threading

con = sl.connect('my-test.db')
c = con.cursor()
stocks_list = []

c.execute('''SELECT * FROM stocks limit 10''')

rows = c.fetchall()


def get_data(row):
    code = row[0].split('/')[-1]
    name = row[0].split('/')[-2]
    url = row[0]
    htmlContent = requests.get(url).content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    if soup.find('div', {'class': 'escnt'}) is not None and soup.find('div', {'class': 'escnt'}).find(
            'div') is not None:
        rating = soup.find('div', {'class': 'escnt'}).find('div').text.split('%')[0]
    else:
        rating = ""
    stocks_list.append({'stock_code': code, 'url': row[0], 'name': name, 'rating': rating})


################# On different threads ###############################
threads = []

for row in rows:
    thread = threading.Thread(target=get_data, args=(row,))
    thread.start()
    threads.append(thread)

for process in threads:
    process.join()

######################### Sequential  ###################################

# for row in rows:
#     get_data(row)


# commetning for testing parallel api calls

c.execute('''CREATE TABLE IF NOT EXISTS money_control_ratings
    (stock_code varchar[50], url varchar[1000], name varchar[1000], rating int);''')

# for stock in stocks_list:
# c.execute("INSERT INTO money_control_ratings VALUES (?,?,?,?)", (stock['stock_code'],stock['url'],stock['name'],stock['rating']))


con.commit()
con.close()
