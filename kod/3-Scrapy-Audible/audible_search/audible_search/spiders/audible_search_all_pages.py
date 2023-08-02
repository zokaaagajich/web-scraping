import os
import sys
import time
from urllib.parse import urlparse, urlunparse

import scrapy
from audible_search.spiders import \
    audible_search_shared_methods as audible_shared
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors import LinkExtractor as DefaultLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
from urllib.parse import parse_qs, urlencode

import helpers


class CustomLinkExtractor(DefaultLinkExtractor):
    def extract_links(self, response):
        links = super().extract_links(response)
        for link in links:
            # Canonicalize the URL
            url_parts = urlparse(link.url)

            # Parse the query string and keep only the 'node' and 'page' parameters
            query = parse_qs(url_parts.query)
            query_to_keep = {param: query[param] for param in ('node', 'page') if param in query}
            canonical_query = urlencode(query_to_keep, doseq=True)

            # Create the canonical URL
            link.url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, "", canonical_query, ""))

        return links
    
class AudibleSearchAllPages(CrawlSpider):
    name = 'audible_search_all_pages'
    allowed_domains = ['www.audible.com']
    start_urls = ['http://www.audible.com/search']

    book_titles = [] 
    book_authors = [] 
    book_release_dates = []
    book_prices = []
    start_time = 0
    books_scraped = 0

    # Setting an user-agent variable
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

    # Setting rules for the crawler
    rules = (
        Rule(CustomLinkExtractor(
            restrict_xpaths=("//div[contains(@class, 'categories')]//a", "//span[contains(@class, 'nextButton')]//a")),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        if not self.start_time:
            self.start_time = time.time()

        container = response.css('div.adbl-impression-container')
        titles, authors, release_dates, prices = audible_shared.collect_books_info(container)
        num_books = len(titles)
        self.book_titles.extend(titles)
        self.book_authors.extend(authors)
        self.book_release_dates.extend(release_dates)
        self.book_prices.extend(prices)

        self.books_scraped += num_books
        if self.books_scraped >= 12000:
            raise scrapy.exceptions.CloseSpider("Reached book scraping limit: 12000")

    def closed(self, reason):
        end_time = time.time()
        execution_time = end_time - self.start_time
        print(f"Execution time: {execution_time} seconds")

        helpers.export_data_as_csv('books-scraped-all-pages.csv', self.book_titles, self.book_authors, self.book_release_dates, self.book_prices)
