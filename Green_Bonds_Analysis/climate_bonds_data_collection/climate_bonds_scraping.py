from bs4 import BeautifulSoup as bs
from requests import get
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import sqlite3


# Defining the data class
@dataclass
class ClimateBondData:
    bond_id: str
    entity: str
    amount_issued: int
    currency: str
    issue_date: datetime
    maturity_date: Optional[datetime] = None
    cbi_certified: Optional[str] = None
    spo_provider: Optional[str] = None


# Connect to SQLite database
conn = sqlite3.connect('/Green_Bonds_Analysis/sql_databases/climate_bonds_data.db')
cursor = conn.cursor()
# Create table to store data
cursor.execute('''CREATE TABLE IF NOT EXISTS climate_bonds_data (
                    bond_id TEXT,
                    entity TEXT,
                    amount_issued INTEGER,
                    currency TEXT,
                    issue_date DATETIME,
                    maturity_date DATETIME,  -- Allow NULL for optional value
                    cbi_certified TEXT,  -- Allow NULL for optional value
                    spo_provider TEXT  -- Allow NULL for optional value
                )''')


# Scraping the climate bonds website
link = 'https://www.climatebonds.net/cbi/pub/data/bonds?items_per_page=All'


# Defining function to scrape data
def get_climate_data(link: str) -> List[ClimateBondData]:
    page_data = get(link).text
    soup = bs(page_data, 'html.parser')

    html_data_list = soup.find_all('tr', {'class': ['odd', 'even', 'odd views-row-first',
                                                    'even views-row-last']})
    print(f'Items found- {len(html_data_list)}')
    climate_data_list = []
    for html_data in html_data_list:
        climate_data = ClimateBondData(bond_id=get_bond_id(html=html_data),
                                       entity=get_entity(html=html_data),
                                       amount_issued=get_amount_issued(html=html_data),
                                       currency=get_currency(html=html_data),
                                       issue_date=get_issue_date(html=html_data),
                                       maturity_date=get_maturity_date(html=html_data),
                                       cbi_certified=get_cbi_certified(html=html_data),
                                       spo_provider=get_spo_provider(html=html_data)
                                       )
        # Store data in database
        cursor.execute('''INSERT INTO climate_bonds_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (climate_data.bond_id, climate_data.entity, climate_data.amount_issued, climate_data.currency,
                        climate_data.issue_date, climate_data.maturity_date, climate_data.cbi_certified, climate_data.spo_provider
                        ))
        conn.commit()
        climate_data_list.append(climate_data)
    return climate_data_list


def get_bond_id(html: bs):
    bond_id = html.find('td', class_ ='views-field views-field-title views-align-left').text.strip()
    return bond_id


def get_entity(html: bs):
    entity = html.find('td', class_ ='views-field views-field-field-bond-entity').text.strip()
    return entity


def get_amount_issued(html: bs):
    try:
        amount_issued = int((html.find('td', class_ ='views-field views-field-field-bond-amt-issued views-align-right')
                      .text.replace(',', '')).strip())
    except:
        amount_issued = None
    return amount_issued


def get_currency(html: bs):
    currency = html.find('td', class_ ='views-field views-field-field-bond-currency views-align-left').text.strip()
    return currency


def get_issue_date(html: bs):
    issue_date = html.find('td', class_ ='views-field views-field-field-bond-issue-date active views-align-right').text.strip()
    issue_date_str = "01-" + issue_date
    date_obj = datetime.strptime(issue_date_str, "%d-%b-%y")
    return date_obj


def get_maturity_date(html: bs):
    try:
        maturity_date = html.find('td', class_ ='views-field views-field-field-bond-maturity-date').text.strip()
        maturity_date_str = "01-" + maturity_date
        date_obj = datetime.strptime(maturity_date_str, "%d-%b-%y")
        return date_obj
    except:
        return None


def get_cbi_certified(html: bs):
    try:
        cbi_certified = html.find('td', class_ ='views-field views-field-field-bond-verifier').text.strip()
        return cbi_certified
    except:
        return None


def get_spo_provider(html: bs):
    try:
        spo_provider = html.find('td', class_ ='views-field views-field-field-bond-spo-provider').text.strip()
        return spo_provider
    except:
        return None


def main():
    get_climate_data(link=link)


if __name__ == "__main__":
    main()


# Close database connection
conn.close()