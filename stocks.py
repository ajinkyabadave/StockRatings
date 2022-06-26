from nsetools import Nse
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import string
import sqlite3 as sl

nse = Nse()
all_stock_codes = nse.get_stock_codes()
stocks_list = []
con = sl.connect('my-test.db')
c = con.cursor()   

c.execute('''CREATE TABLE IF NOT EXISTS stocks(url varchar[1000]);''')




for alphabet in string.ascii_uppercase:
    now = datetime.now().time() # time object
    print(now)	
    url = 'https://www.moneycontrol.com/india/stockpricequote/' + alphabet
    stock_lists_page = requests.get(url)
    soup = BeautifulSoup(stock_lists_page.content, 'html5lib') 
    table = soup.find('table', {'class': 'pcq_tbl MT10'})

    for row in table.findAll('a'):
        stocks_list.append(row['href'])


# to check for just one alphabet

# url = 'https://www.moneycontrol.com/india/stockpricequote/A' 
# stock_lists_page = requests.get(url)
# soup = BeautifulSoup(stock_lists_page.content, 'html5lib')
# table = soup.find('table', {'class': 'pcq_tbl MT10'})
# # print(table.prettify())

for row in table.findAll('a'):
    stocks_list.append(row['href'])

    
while("" in stocks_list) :
    stocks_list.remove("")
# c.executemany('INSERT INTO stocks VALUES(?)', (stocks_list))

for stock in stocks_list:
    c.execute("INSERT INTO stocks VALUES (?)", (stock,))

con.commit();
con.close();