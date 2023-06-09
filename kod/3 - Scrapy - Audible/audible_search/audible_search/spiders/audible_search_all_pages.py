import os
import sys

import scrapy
from audible_search.spiders import \
    audible_search_shared_methods as audible_shared
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
import helpers


class AudibleSearchAllPages(CrawlSpider):
    name = 'audible_search_all_pages'
    allowed_domains = ['www.audible.com']
    start_urls = ['http://www.audible.com/search']

    book_titles = [] 
    book_authors = [] 
    book_release_dates = []
    book_prices = []

    # Setting an user-agent variable
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

    # Editing the user-agent in the request sent
    def start_requests(self):
        yield scrapy.Request(url='http://www.audible.com/search', headers={
            'user-agent':self.user_agent
        })

    # Setting rules for the crawler
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[contains(@class, 'categories')]//a")), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    # Setting the user-agent
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
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
        helpers.export_data_as_csv('books-scraped-all-pages.csv', self.book_titles, self.book_authors, self.book_release_dates, self.book_prices)

