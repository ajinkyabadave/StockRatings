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

soup = BeautifulSoup(opener.open(sectors_url,timeout=10).read() , 'html.parser')
cards = soup.find('div', {'class': 'card cardscreen cardsmall'}).findAll('a')


print(cards)
company_urls = []
for card in cards:
    sectors_list.append(finology_base_url + card['href'])

for sector in sectors_list:
    print(sector)
    company_urls = []
    soup = BeautifulSoup(opener.open(sector,timeout=10).read(), 'html.parser')
    link_tags = soup.findAll('table')[0].findAll('a')
    for link in link_tags:
        company_urls.append(link['href'])

for url in company_urls:
    stocks_list.append(finology_base_url + url)
print(stocks_list)       


soup = BeautifulSoup(opener.open("https://ticker.finology.in/company/WENDT",timeout=10).read() , 'html.parser')
overall_rating = soup.find('span',{'id':'mainContent_ltrlOverAllRating'})['style'].split(":")[1].replace(";","")
management_rating =  soup.find('div',{'id':'mainContent_ManagementRating'})['style'].split(":")[1].replace(";","")
valuation_rating = soup.find('div',{'id':'mainContent_ValuationRating'})['style'].split(":")[1].replace(";","")
efficiency_rating = soup.find('div',{'id':'mainContent_EfficiencyRating'})['style'].split(":")[1].replace(";","")
financials_rating = soup.find('div',{'id':'mainContent_FinancialsRating'})['style'].split(":")[1].replace(";","")
