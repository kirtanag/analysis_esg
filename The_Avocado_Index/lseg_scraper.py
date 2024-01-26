import time
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
from typing import List
import sqlite3
import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver(headless: bool = True, chrome_version: int = 120) -> WebDriver:
  driver = uc.Chrome(headless=headless, version_main=chrome_version)#, use_subprocess=False)
  return driver

URL = 'https://www.londonstockexchange.com/indices/ftse-100/constituents/table'

 # Connect to SQL
conn = sqlite3.connect('ftse_100_companies.db')
cursor = conn.cursor()
# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS ftse_100_companies (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    market_cap FLOAT NOT NULL,
                    price FLOAT NOT NULL,
                    change FLOAT NOT NULL,
                    change_percent TEXT NOT NULL)''')


# Commit changes
conn.commit()


@dataclass
class FtseData:
  code: str
  name: str
  currency: str
  market_cap: float
  price: float
  change: float
  change_percent: str


def store_data(data: List[FtseData]):
  for company in data:
    cursor.execute('''INSERT INTO ftse_100_companies 
                        (code, name, currency, market_cap, price, change, change_percent)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (company.code, company.name, company.currency,
                    company.market_cap, company.price, company.change,
                    company.change_percent))
  # Commit changes
  conn.commit()


def get_data_from_page(html_soup: str) -> List[FtseData]:
  data_from_page = []
  soup = BeautifulSoup(html_soup, "html.parser")
  ftse_company_details = soup.find_all("tr", class_='medium-font-weight slide-panel')
  for ftse_company in ftse_company_details:
    code = ftse_company.find("td", class_='clickable bold-font-weight instrument-tidm gtm-trackable td-with-link').text
    name = ftse_company.find("td", class_='clickable instrument-name gtm-trackable td-with-link').text
    currency = ftse_company.find("td", class_='instrument-currency hide-on-landscape').text
    market_cap = ftse_company.find("td", class_='instrument-marketcapitalization hide-on-landscape').text
    price = ftse_company.find("td", class_='instrument-lastprice').text
    try:
        change = ftse_company.find("td", class_='instrument-netchange hide-on-landscape positivechange').text
    except:
        change = ftse_company.find("td", class_='instrument-netchange hide-on-landscape negativechange').text
    change_percent = ftse_company.find("td", class_='instrument-percentualchange hide-on-landscape gtm-trackable').text
    ftse_company_detail = FtseData(code = code,
                                   name = name,
                                   currency = currency,
                                   market_cap = market_cap,
                                   price = price,
                                   change = change,
                                   change_percent = change_percent
                                   )
    logging.info(f'Captured details for company code {code}')
    data_from_page.append(ftse_company_detail)
  return data_from_page

def scraper_for_ftse_100(url: str) -> List[FtseData]:
  driver = get_driver(headless=False, chrome_version=120)
  driver.get(url)
  time.sleep(20)
  wait = WebDriverWait(driver, 120)
  reject_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler')))
  reject_button.click()
  page_source = driver.page_source
  data_from_page = get_data_from_page(page_source)
  return data_from_page


def get_all_ftse_100_companies(pages: List[int], first_url: str) -> List[FtseData]:
    all_data = []
    for page in pages:
        url = f'{first_url}?page={page}'
        logging.info(f'Scraping data from page: {page}')
        data_from_page = scraper_for_ftse_100(url)
        all_data.extend(data_from_page)
    store_data(all_data)
    return all_data

def main():
    URL = 'https://www.londonstockexchange.com/indices/ftse-100/constituents/table'
    pages = [1, 2, 3, 4, 5]
    result = get_all_ftse_100_companies(pages, URL)
    print(result)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()