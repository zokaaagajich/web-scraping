import os
import sys

import scrapy
from audible_search.spiders import \
    audible_search_shared_methods as audible_shared

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
import helpers


class AudibleSearchSinglePageSpider(scrapy.Spider):
    name = 'audible_search_single_page'
    allowed_domains = ['www.audible.com']
    start_urls = ['https://www.audible.com/search']

    def parse(self, response):
        container = response.css('div.adbl-impression-container')
        book_titles, book_authors, book_release_dates, book_prices = audible_shared.collect_books_info(container)
        helpers.export_data_as_csv('books-scraped-single-page.csv', book_titles, book_authors, book_release_dates, book_prices)

        yield {
            'book_titles': book_titles, 
            'book_authors': book_authors, 
            'book_release_dates': book_release_dates, 
            'book_prices': book_prices
        }
