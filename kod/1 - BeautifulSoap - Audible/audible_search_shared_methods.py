import re

import pandas as pd
import requests


def fetch_html(url):
    try: 
        response = requests.get(url) 
    except requests.exceptions.RequestException:
        print("Error fetching page")
        exit()    

    return response.text

def substr_after_colon(str): 
    colon_index = str.index(":")
    return str[colon_index + 1:].strip()

def extract_regular_price(str):
    pattern = r"\s*Regular price:\s*\$([\d.]+)\s*"
    matches = re.search(pattern, str)

    if matches:
        return round(float(matches.group(1)))

def get_last_page(soup):
    pagination = soup.find('ul', class_='pagingElements')
    pages = pagination.find_all('li', class_='bc-list-item')
    return pages[-2].text

def collect_books_info(container) :
    book_titles = []
    book_authors = []
    book_release_dates = []
    book_prices = []

    book_list = container.find_all('li', class_='productListItem')
    for book in book_list:
        book_titles.append(book.find('h3', class_='bc-heading').text.strip())
        book_authors.append(book.find('li', class_='authorLabel').a.text.strip())
        book_release_dates.append(substr_after_colon(book.find('li', class_='releaseDateLabel').text.strip()))

        price_element = book.find('div', class_='adblBuyBoxPrice')
        if price_element is not None:
            book_prices.append(extract_regular_price(price_element.text.strip()))
        else:
            book_prices.append('-') 

    return book_titles, book_authors, book_release_dates, book_prices,

def export_data_as_csv(name, titles, authors, release_dates, prices):
    df = pd.DataFrame({
        'Title': titles, 
        'Author': authors,
        'Release date': release_dates,
        'Price $': prices,
    })

    df.to_csv(name)
    print(df)