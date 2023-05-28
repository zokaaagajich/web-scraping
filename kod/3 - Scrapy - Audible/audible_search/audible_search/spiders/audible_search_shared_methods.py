import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))
import helpers


def collect_books_info(response):
    book_titles = []
    book_authors = []
    book_release_dates = []
    book_prices = []
    
    book_list = response.xpath('//li[contains(@class, "productListItem")]')

    for book in book_list:
        book_titles.append(book.xpath('.//h3[contains(@class, "bc-heading")]').css('a::text').get().strip())
        book_authors.append(book.xpath('.//li[contains(@class, "authorLabel")]').css('a::text').get().strip())
        book_release_dates.append(helpers.substr_after_colon(book.xpath('//li[contains(@class, "releaseDateLabel")]').css('span::text').get().strip()))
        price_element = book.xpath('.//div[contains(@class, "adblBuyBoxPrice")]').xpath('.//p[contains(@class, "buybox-regular-price")]').css('span::text').getall()
        
        if price_element:
            book_prices.append(helpers.extract_regular_price(' '.join(price_element).strip()))
        else:
            book_prices.append('-') 

    return book_titles, book_authors, book_release_dates, book_prices
