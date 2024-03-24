from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from gnews import GNews
from requests import get
import sqlite3


# Creating a dataclass to neatly structure and store down news articles
@dataclass
class NewsFormatted:
    title: str
    description: str
    published_date: datetime
    url: str
    publisher_href: str
    publisher_title: str
    news_body: Optional[str] = None


# Defining the function to go grab and format news around ESG for a company
def get_all_news(company: str) -> List[NewsFormatted]:
    # Connect to SQLite database
    conn = sqlite3.connect(f'/Users/kirtanagopakumar/PycharmProjects/analysis_esg/Green_Bonds_Analysis/sql_databases/{company}_news_data.db')
    cursor = conn.cursor()
    # Create table to store data
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {company}_news_data (
                        title TEXT,
                        description TEXT,
                        published_date DATETIME,
                        url TEXT,
                        publisher_href TEXT,
                        publisher_title TEXT,
                        news_body TEXT  -- Allow NULL for optional value
                    )''')
    keywords = ['ESG', 'green initiative', 'green initiatives', 'climate', 'sustainability', 'sustainable',
                'responsible investing'] # Keywords we care about in the context of the company
    google_news = GNews()
    news_found = []
    for keyword in keywords:
        news = google_news.get_news(f'{company}+{keyword}')
        news_found.append(news)
    # Formatting the news gathered and only keeping unique articles
    formatted_news = []
    unique_links = set()
    flattened_news_found = [item for news_dict in news_found for item in news_dict]

    for news in flattened_news_found:
        if news['url'] not in unique_links:
            unique_links.add(news['url'])
            news_item = NewsFormatted(title=news['title'],
                                           description=news['description'],
                                           published_date=news['published date'],
                                           url=news['url'],
                                           publisher_href=news['publisher']['href'],
                                           publisher_title=news['publisher']['title'],
                                           news_body=None)
            # Store data in database
            cursor.execute(f'''INSERT INTO {company}_news_data VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (
                           news_item.title, news_item.description, news_item.published_date, news_item.url,
                           news_item.publisher_href, news_item.publisher_title, None
                           ))
            conn.commit()
            formatted_news.append(news_item)
    # Close database connection
    conn.close()
    return formatted_news

