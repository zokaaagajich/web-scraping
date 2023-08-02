import sys
import time

sys.path.append('../')

import audible_search_shared_methods as audible_shared
import helpers
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

book_titles = []
book_authors = []
book_release_dates = []
book_prices = []

def main():
    start_time = time.time()

    # Initialize the driver
    driver = audible_shared.initialize_driver()
    website = 'https://www.audible.com/search'
    driver.get(website)

    # pagination
    pagination = driver.find_element(By.XPATH, value='//ul[contains(@class, "pagingElements")]')
    pages = pagination.find_elements(By.TAG_NAME, value='li')
    last_page = int(pages[-2].get_attribute("innerText"))
    current_page = 1

    while current_page <= last_page:
        container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
        titles, authors, release_dates, prices = audible_shared.collect_books_info(container)
        book_titles.extend(titles)
        book_authors.extend(authors)
        book_release_dates.extend(release_dates)
        book_prices.extend(prices)
        driver.get(website + '?page=' + str(current_page))
        current_page += 1

        # try:
        #     next_page = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "nextButton")]')))
        #     next_page.click()
        # except:
        #     print('Failed to find or click the next button, so navigating via URL')
        #     pass

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    driver.quit()

    helpers.export_data_as_csv('books-scraped-multiple-pages.csv', book_titles, book_authors, book_release_dates, book_prices)

if __name__ == "__main__":
    main()