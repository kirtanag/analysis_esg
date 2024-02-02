import time
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
from typing import List
import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

def get_driver(headless: bool = True, chrome_version: int = 120) -> WebDriver:
  driver = uc.Chrome(headless=headless, version_main=chrome_version)
  return driver


 # Connect to SQL
conn = sqlite3.connect('../sql_databases/ftse_100_industries_from_lseg.db')
cursor = conn.cursor()
# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS ftse_100_industries_from_lseg (
                    code TEXT PRIMARY KEY,
                    industry TEXT NOT NULL)''')
conn.commit()

@dataclass
class FtseIndustryData:
  code: str
  industry: str

def store_data(data: FtseIndustryData):
    try:
      cursor.execute('''INSERT INTO ftse_100_industries_from_lseg 
                          (code, industry)
                          VALUES (?, ?)''',
                     (data.code, data.industry))
      # Commit changes
      conn.commit()
    except:
      pass

def get_href_from_page(html_soup: str) -> List[str]:
  soup = BeautifulSoup(html_soup, "html.parser")
  ftse_company_details = soup.find_all("tr", class_='medium-font-weight slide-panel')
  codes = [company.find("td", class_='clickable bold-font-weight instrument-tidm gtm-trackable td-with-link').text
           for company in ftse_company_details]
  href_from_page = [
      company.find("a", class_='dash-link black-link ellipsed').attrs['href']
      for company in ftse_company_details
  ]
  return codes, href_from_page

def scraper_for_ftse_100(url: str) -> str:  # Now returns HTML content
  driver = get_driver(headless=False, chrome_version=120)
  driver.get(url)
  time.sleep(20)
  wait = WebDriverWait(driver, 120)
  reject_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler')))
  reject_button.click()
  html_content = driver.page_source
  driver.quit()  # Close the browser
  return html_content

def get_all_ftse_100_companies_industries(pages: List[int], first_url: str) -> List[FtseIndustryData]:
  all_data = []
  for page in pages:
    url = f'{first_url}?page={page}'
    logging.info(f'Scraping data from page: {page}')
    (code, data_from_page) = get_href_from_page(scraper_for_ftse_100(url))
    all_data.extend(data_from_page)

  url_list = []
  for link in range(len(all_data)):
    # if link > 3:
      link_industry = f'https://www.londonstockexchange.com/{all_data[link]}/our-story'
      print(link_industry)
      code_company = code[link]
      industry_data = scraper_for_ftse_100(url=link_industry)
      soup = BeautifulSoup(industry_data, "html.parser")
      industry = soup.find("div", id='ccc-data-ftse-industry').text.replace('FTSE industry', '').strip()
      url_list.append(FtseIndustryData(code = code_company, industry=industry))
      print(FtseIndustryData(code = code_company, industry=industry))
      store_data(FtseIndustryData(code = code_company, industry=industry))
  return url_list

def main():
  URL = 'https://www.londonstockexchange.com/indices/ftse-100/constituents/table'
  pages = [4]#, 3, 4, 5]  # Uncomment for all pages
  industries = get_all_ftse_100_companies_industries(pages, URL)
  print(industries)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

