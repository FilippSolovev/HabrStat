import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import dateparser


def _fetch_habr_feed_page(page_num):
    url = 'https://habr.com/all/'
    if page_num:
        url += f'page{page_num}/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print('Timeout error!')
        sys.exit()
    except requests.RequestException:
        print('Download error!')
        sys.exit()
    else:
        return response.text


def fetch_raw_habr_feed(pages=10):
    raw_pages = []
    for page_num in range(pages):
        raw_pages.append(_fetch_habr_feed_page(page_num=page_num))
    return raw_pages


def parse_habr_page(raw_page):
    """Creates a dataframe with article titles and times they were posted"""
    dataframe_out_of_page = pd.DataFrame(columns=['date', 'title'])
    soup = BeautifulSoup(raw_page, "html.parser")
    for article_block in soup.find_all(
        'article',
        {'class': 'post post_preview'},
    ):
        date_str = article_block.find('span', {'class': 'post__time'})
        date = dateparser.parse(date_str.contents[0], languages=['ru'])
        title = article_block.find('a', {'class': 'post__title_link'})
        dataframe_out_of_page = dataframe_out_of_page.append({
            'date': date,
            'title': title.contents[0],
        }, ignore_index=True)
    return dataframe_out_of_page


def get_data(pages=10):
    raw_pages = fetch_raw_habr_feed(pages)
    list_of_dataframes = []
    for raw_page in raw_pages:
        list_of_dataframes.append(parse_habr_page(raw_page))
    # Merging dataframes into one and resetting an index
    data = pd.concat(list_of_dataframes, ignore_index=True)
    # Setting date as index
    data = data.set_index('date')
    return data
