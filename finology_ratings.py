from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sqlite3 as sl
import os
import ssl
import platform
import urllib

# ...

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_default_certs()

if platform.system().lower() == 'darwin':
    import certifi
    ssl_context.load_verify_locations(
        cafile=os.path.relpath(certifi.where()),
        capath=None,
        cadata=None)

# previous context
https_handler = urllib.request.HTTPSHandler(context=ssl_context)

opener = urllib.request.build_opener(https_handler)





con = sl.connect('my-test.db')
c = con.cursor()  
stocks_list = []
sectors_list = []

finology_base_url = 'https://ticker.finology.in'
sectors_url = finology_base_url + '/sector'

soup = BeautifulSoup(opener.open(sectors_url,timeout=10).read() , 'html5lib')
cards = soup.find('div', {'class': 'card cardscreen cardsmall'}).findAll('a')


print(cards)
for card in cards:
    sectors_list.append(finology_base_url + card['href'])

for sector in sectors_list:
    print(sector)
    soup = BeautifulSoup(opener.open(sector,timeout=10).read(), 'html5lib')
    # print(soup.findAll('table',{'id':'companylist'}).find('tbody'))
    if soup.find('tbody') is not None and soup.find('tbody').findAll('tr'):
     is not None and soup.find('tbody').findAll('td').find('a') is not None:
        stocks_list.append( finology_base_url + soup.find('tbody').findAll('td').find('a'))


print(stocks_list)       
