import os
import sys
import time

import scrapy
from audible_search.spiders import \
    audible_search_shared_methods as audible_shared

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
import helpers


class AudibleSearchMultiplePagesPySpider(scrapy.Spider):
    name = 'audible_search_multiple_pages'
    allowed_domains = ['www.audible.com']
    start_urls = ['http://www.audible.com/search']

    book_titles = [] 
    book_authors = [] 
    book_release_dates = []
    book_prices = []
    start_time = 0

    def parse(self, response):
        if not self.start_time:
            self.start_time = time.time()

        container = response.css('div.adbl-impression-container')
        titles, authors, release_dates, prices = audible_shared.collect_books_info(container)
        self.book_titles.extend(titles)
        self.book_authors.extend(authors)
        self.book_release_dates.extend(release_dates)
        self.book_prices.extend(prices)

        next_page_url = 'http://www.audible.com' + response.xpath('//span[contains(@class, "nextButton")]//a/@href').get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)     

    def closed(self, reason):
        end_time = time.time()
        execution_time = end_time - self.start_time
        print(f"Execution time: {execution_time} seconds")

        helpers.export_data_as_csv('books-scraped-multiple-pages.csv', self.book_titles, self.book_authors, self.book_release_dates, self.book_prices)
