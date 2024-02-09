import requests
from tqdm import tqdm
import sqlite3
import re

# Function to get images from a Wikipedia page
# Function to get images from a Wikipedia page
def get_images_from_page(page_title):
    img_links = {}
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    # First, retrieve the image names
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "images"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA['query']['pages']

    # Then, retrieve the image information including the direct links
    for k, v in PAGES.items():
        image_link_for_company = []
        company_name = page_title
        for img in v['images']:
            image_title = img["title"]
            PARAMS = {
                "action": "query",
                "format": "json",
                "titles": image_title,
                "prop": "imageinfo",
                "iiprop": "url"
            }
            R = S.get(url=URL, params=PARAMS)
            image_data = R.json()
            image_info = image_data['query']['pages']
            for _, v in image_info.items():
                if 'imageinfo' in v:
                    image_url = v['imageinfo'][0]['url']
                    image_link_for_company.append(image_url)
        # First, check if any URL contains both 'logo' and the company name
        for url in image_link_for_company:
            if 'logo' in url.lower() and company_name.lower() in url.lower():
                return company_name, url
                break
            else:
                # If no such URL is found, check for any 'logo' URL without 'commons-logo' in the title
                for url in image_link_for_company:
                    if 'logo' in url.lower() and 'commons-logo' not in url.lower():
                        return company_name, url
                        break
                else:
                    # If no such URL is found, check for any URL containing the company name
                    for url in image_link_for_company:
                        if company_name.lower() in url.lower():
                            return company_name, url
                            break
                    else:
                        return company_name, "No match found"

# Function to extract links from a specific section of the Wikipedia page
def get_links_from_section(page_title, section):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "parse",
        "page": page_title,
        "prop": "links",
        "section": section,
        "format": "json"
    }
    response = S.get(url=URL, params=PARAMS)
    data = response.json()
    links = []
    for link in data['parse']['links']:
        if link['ns'] == 0:  # Namespace 0 corresponds to Wikipedia articles
            links.append(link['*'])
    return links


def get_tickers_and_page_names_from_ftse100_page(page_title):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "parse",
        "page": page_title,
        "prop": "wikitext",
        "format": "json"
    }
    response = S.get(url=URL, params=PARAMS)
    data = response.json()

    wikitext = data['parse']['wikitext']['*']

    # Use regex to extract ticker symbols from the wikitext
    tickers = re.findall(r'\[\[(.+?)\]\]\s*\|\|\s*(.+?)\s*\|\|', wikitext)

    # Filter out tickers with empty values
    tickers = [(company.strip(), ticker.strip()) for company, ticker in tickers if ticker.strip()]

    return tickers


tickers = get_tickers_and_page_names_from_ftse100_page('FTSE 100 Index')
print(len(tickers))


# Get the links from the specified section
page_title = "FTSE_100_Index"
section = 6
constituents_links = get_links_from_section(page_title, section)
tickers = get_tickers_and_page_names_from_ftse100_page(page_title)


# Get images from each linked page
company_logos = {}
for link in tqdm(constituents_links, desc="Fetching images"):
    company, url = get_images_from_page(link)
    company_logos[company] = url

# Manually replacing 23 incorrect ones (success rate 77%)
# Replacing the URLs that are unavailable
company_logos['Barclays'] = 'https://en.wikipedia.org/wiki/Barclays#/media/File:Barclays_logo.svg'
company_logos['Compass Group'] = 'https://en.wikipedia.org/wiki/Compass_Group#/media/File:Compass_Group.svg'
company_logos['Diageo'] = 'https://en.wikipedia.org/wiki/Diageo#/media/File:Diageo.svg'
company_logos['Fresnillo plc'] = 'https://en.wikipedia.org/wiki/Fresnillo_plc#/media/File:Fresnillo.svg'
company_logos['HSBC'] = 'https://en.wikipedia.org/wiki/HSBC#/media/File:HSBC_logo_(2018).svg'
company_logos['Kingfisher plc'] = 'https://en.wikipedia.org/wiki/Kingfisher_plc#/media/File:Kingfisher_plc.svg'
company_logos['Legal & General'] = 'https://en.wikipedia.org/wiki/Legal_%26_General#/media/File:Legal_&_General_wordmark.svg'
company_logos['Lloyds Banking Group'] = 'https://en.wikipedia.org/wiki/Lloyds_Banking_Group#/media/File:Lloyds_Banking_Group_logo.svg'
company_logos['London Stock Exchange Group'] = 'https://en.wikipedia.org/wiki/London_Stock_Exchange_Group#/media/File:London_Stock_Exchange_Group_logo.svg'
company_logos['Marks & Spencer'] = 'https://en.wikipedia.org/wiki/Marks_%26_Spencer#/media/File:M&S_logo.svg'
company_logos['Prudential plc'] = 'https://en.wikipedia.org/wiki/Prudential_plc#/media/File:Prudential-plc-1986.svg'
company_logos['Rio Tinto (corporation)'] = 'https://en.wikipedia.org/wiki/Rio_Tinto_(corporation)#/media/File:Rio_Tinto_(corporation)_Logo.svg'
company_logos['Rolls-Royce Holdings'] = 'https://en.wikipedia.org/wiki/Rolls-Royce_Holdings#/media/File:Rolls_royce_holdings_logo.svg'
company_logos['SSE plc'] = 'https://en.wikipedia.org/wiki/SSE_plc#/media/File:SSEenergy.svg'
company_logos["Sainsbury's"] = "https://en.wikipedia.org/wiki/Sainsbury%27s#/media/File:Sainsbury's_Logo.svg"
company_logos['Shell plc'] = 'https://en.wikipedia.org/wiki/Shell_plc#/media/File:Shell_logo.svg'
company_logos['Smith & Nephew'] = 'https://en.wikipedia.org/wiki/Smith_%26_Nephew#/media/File:Smith_nephew.svg'
company_logos['Smiths Group'] = 'https://en.wikipedia.org/wiki/Smiths_Group#/media/File:Smiths_Group.svg'
company_logos['Standard Chartered'] = 'https://en.wikipedia.org/wiki/Standard_Chartered#/media/File:Standard_Chartered_(2021).svg'
company_logos['Tesco'] = 'https://en.wikipedia.org/wiki/Tesco#/media/File:Tesco_Logo.svg'
company_logos['Unilever'] = 'https://en.wikipedia.org/wiki/Unilever#/media/File:Unilever.svg'
company_logos['Vodafone'] = 'https://en.wikipedia.org/wiki/Vodafone#/media/File:Vodafone_2017_logo.svg'
company_logos['Whitbread'] = 'https://en.wikipedia.org/wiki/Whitbread#/media/File:Whitbread_logo_(new).svg'


# Map the companies to their tickers
# Put together with the tickers
for company, ticker in tickers:
    if company in company_logos.keys():
        company_logos[ticker] = company_logos.pop(company)
    else:
        # Check if any item in img.keys() matches a substring of the company name
        matched_key = next((key for key in company_logos.keys() if key in company), None)
        if matched_key:
            company_logos[ticker.replace('-', '.')] = company_logos.pop(matched_key)
# Create a new dictionary to store the modified keys
modified_imgs = {}

# Update the keys in the new dictionary
for k, v in company_logos.items():
    if len(k) == 2:
        modified_k = f'{k}.'
        modified_imgs[modified_k] = v
    else:
        modified_imgs[k] = v

# Replace the original dictionary with the modified one
company_logos = modified_imgs

# Altering our SQL database and storing down the URLs as a new column
# Connect to SQL
conn = sqlite3.connect('../sql_databases/ftse_100_companies_from_lseg.db')
cursor = conn.cursor()
# Modify the table to add a new column for logo URLs
cursor.execute('''ALTER TABLE ftse_100_companies_from_lseg
                  ADD COLUMN logo_url TEXT''')
conn.commit()

cursor.execute('''SELECT code FROM ftse_100_companies_from_lseg''')
existing_company_codes = [row[0] for row in cursor.fetchall()]

for ticker, logo_url in company_logos.items():
    if ticker in existing_company_codes:
        cursor.execute('''UPDATE ftse_100_companies_from_lseg
                          SET logo_url = ?
                          WHERE code = ?''', (logo_url, ticker))
conn.commit()