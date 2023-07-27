import sys
import time

sys.path.append('../')

import audible_search_shared_methods as audible_shared
import helpers
from selenium.webdriver.common.by import By


def main():
    start_time = time.time()

    # Initialize the driver
    driver = audible_shared.initialize_driver()
    website = 'https://www.audible.com/search'
    driver.get(website)

    container = driver.find_element(By.CLASS_NAME, value='adbl-impression-container ')
    book_titles, book_authors, book_release_dates, book_prices = audible_shared.collect_books_info(container)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    driver.quit()

    helpers.export_data_as_csv('books-scraped-single-page.csv', book_titles, book_authors, book_release_dates, book_prices)

if __name__ == "__main__":
    main()