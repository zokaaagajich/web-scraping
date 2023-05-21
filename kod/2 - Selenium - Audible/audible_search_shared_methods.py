import random

import helpers
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def initialize_driver():
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    user_agent = random.choice(user_agent_list)

    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('window-size=1920x1080')

    path = '/usr/local/bin/chromedriver_mac64_arm64/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def collect_books_info(container):
    book_titles = []
    book_authors = []
    book_release_dates = []
    book_prices = []
    
    book_list = container.find_elements(By.XPATH, value='.//li[contains(@class, "productListItem")]')

    for book in book_list:
        book_titles.append(book.find_element(By.XPATH, value='.//h3[contains(@class, "bc-heading")]').text.strip())
        book_authors.append(book.find_element(By.XPATH, value='.//li[contains(@class, "authorLabel")]').find_element(By.TAG_NAME, 'a').get_attribute('innerHTML'))
        book_release_dates.append(helpers.substr_after_colon(book.find_element(By.XPATH, value='.//li[contains(@class, "releaseDateLabel")]').text.strip()))
        
        price_element = book.find_element(By.XPATH, value='.//div[contains(@class, "adblBuyBoxPrice")]')
        if price_element is not None:
            book_prices.append(helpers.extract_regular_price(price_element.text.strip()))
        else:
            book_prices.append('-') 

    return book_titles, book_authors, book_release_dates, book_prices,
