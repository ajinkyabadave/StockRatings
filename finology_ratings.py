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


def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS finology_sectors
        (sector_url varchar[1000], sector_name varchar[100]);''')

    c.execute('''CREATE TABLE IF NOT EXISTS finology_ratings
        (stock_code varchar[50], stock_url varchar[1000], name varchar[1000],sector_name varchar[100], overall_rating real,
        management_rating real, valuation_rating real, efficiency_rating real, financials_rating real );''')

def fetch_sectors():
    soup = BeautifulSoup(opener.open(sectors_url, timeout=10).read(), 'html.parser')
    cards = soup.findAll('a',{'class':'btn btn-sm btn-primary ml-0'})
    print(cards)
    company_urls = []
    for card in cards:
        sector_url = finology_base_url + card['href']
        sector_name = sector_url.split('sector/')[1]
        # sectors_list.append(sector_url)
        c.execute("INSERT INTO finology_sectors VALUES (?,?)", (sector_url,sector_name,))



def fetch_stock_urls():
    c.execute('''SELECT * FROM finology_sectors''')
    sectors_list = c.fetchall()
    for sector in sectors_list:
        print(sector)
        company_urls = []
        soup = BeautifulSoup(opener.open(sector[0]).read(), 'html.parser')
        tables = soup.findAll('table')
        # link_tags = [table.findAll('a') for table in tables]
        for table in tables:
            link_tags = table.findAll('a')
            for link in link_tags:
                company_url =link['href']
                company_code =company_url.split('company/')[1]
                company_urls.append(company_url)
                c.execute("INSERT INTO finology_ratings(stock_code, stock_url,sector_name) VALUES (?,?,?)",
                          (company_code,company_url,sector[1]))


def fetch_stock_ratings():
    c.execute('''SELECT stock_url FROM finology_ratings''')
    company_urls = list(c.fetchall())
    company_urls = [finology_base_url + url[0] for url in company_urls]
    for url in company_urls:
        print(stocks_list)
        soup = BeautifulSoup(opener.open(url).read(), 'html.parser')
        overall_rating = soup.find('span', {'id': 'mainContent_ltrlOverAllRating'})['style']
        overall_rating = overall_rating.split(":")[1].replace(";", "") if overall_rating is not None else 0
        management_rating = soup.find('div', {'id': 'mainContent_ManagementRating'})['style']
        management_rating = management_rating.split(":")[1].replace(";", "") if management_rating is not None else 0
        valuation_rating = soup.find('div', {'id': 'mainContent_ValuationRating'})['style']
        valuation_rating = valuation_rating.split(":")[1].replace(";", "") if valuation_rating is not None else 0
        efficiency_rating = soup.find('div', {'id': 'mainContent_EfficiencyRating'})['style']
        efficiency_rating = efficiency_rating.split(":")[1].replace(";", "") if efficiency_rating is not None else 0
        financials_rating = soup.find('div', {'id': 'mainContent_FinancialsRating'})['style']
        financials_rating = financials_rating.split(":")[1].replace(";", "") if financials_rating is not None else 0
        c.execute("INSERT INTO finology_ratings(overall_rating, management_rating,valuation_rating,efficiency_rating,financials_rating) "
                  "VALUES (?,?,?,?,?)",
                  (overall_rating, management_rating,valuation_rating,efficiency_rating,financials_rating))


create_tables()
# fetch_sectors()
# fetch_stock_urls()
fetch_stock_ratings()



con.commit()
con.close()
