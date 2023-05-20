import random
import time

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

start_time = time.time()

PRICE_LIMIT = 150
MAX_SCROLL_ATTEMPTS = 5
NIGHTS_SPENT_MIN = 2
NIGHTS_SPENT_MAX = 6

flights_ids = []

departure_dates = []
departure_from_info = []
departure_to_info = []
departure_duration = []
departure_logo = []

return_dates = []
return_from_info = []
return_to_info = []
return_duration = []
return_logo = []

nights_count = []
prices = []

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

def close_cookies_dialog(driver):
    wait = WebDriverWait(driver, 20)
    reject_cookies_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ButtonPrimitiveContentChildren') and contains(text(), 'Reject all')]")))
    reject_cookies_btn.click()
    print('Cookies dialog closed')

def set_anywhere_as_destination_input(driver):
    wait = WebDriverWait(driver, 20)
    # Reach destination input and click on it
    destination_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test='SearchPlaceField-destination']//input")))
    destination_input.click()
    
    # Catch anywhere option within dropdown and click on it
    anywhere_dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test='AnywhereRow']")))
    anywhere_dropdown_option.click()
    print('Anywhere added to destination input')

def get_explore_url(driver):
    wait = WebDriverWait(driver, 20)
    # Get url from Explore btn
    return wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-test='LandingSearchButton']"))).get_attribute('href')

def set_eur_as_currency(driver):
    wait = WebDriverWait(driver, 20)
    # Open currency settings (dialog)
    currency_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='RegionalSettingsButton']")))
    currency_btn.click()

    # Choose currency within dropdown
    currency_dropdown_wait = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@data-test='CurrencySelect']")))
    currency_dropdown = Select(currency_dropdown_wait)
    currency_dropdown.select_by_value('eur')

    # Save currency
    save_currency_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ButtonPrimitiveContentChildren') and contains(text(), 'Save & continue')]")))
    save_currency_btn.click()
    print('Currency updated')

def set_cabin_bag(driver):
    wait = WebDriverWait(driver, 20)
    # Choose 1 cabin bag
    bags = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test='SearchFormFilters-button-bags']")))
    bags.click()

    cabin_bag_increment = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='increment']")))
    cabin_bag_increment.click()
    bags.click()
    print('Bags count updated')

def get_destination_links(driver):
    wait = WebDriverWait(driver, 20)

    destination_links = []
    destination_wrappers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@data-test='PictureCard']")))

    for destination in destination_wrappers:
        price_unparsed = destination.find_element(By.XPATH, value='.//h3/span/span[2]')
        price = int(price_unparsed.text.split(' ')[0])

        if price <= PRICE_LIMIT:
            destination_links.append(destination.get_attribute('href'))

    print('Destination links: ', destination_links)

    return destination_links

def load_more(driver):
    wait = WebDriverWait(driver, 20)
    scroll_attempts = 0  # Counter for scroll attempts
              
    while scroll_attempts < MAX_SCROLL_ATTEMPTS:
        try:
            load_more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ButtonPrimitiveContentChildren') and contains(text(), 'Load more')]")))
            actions = ActionChains(driver)
            actions.move_to_element(load_more_btn).perform()
            load_more_btn.click()
            print('Loaded more')
            time.sleep(5)  # Add a small delay for the new flights to load
            scroll_attempts += 1
        except exceptions.TimeoutException as e:
            print(e)
            break

def check_flight_and_collect_if_conditions_are_met(flight):
    flight_card_left = flight.find_element(By.XPATH, value=".//div[contains(@class, 'ResultCardstyled__ResultCardMain')]")
    flight_card_right = flight.find_element(By.XPATH, value=".//div[@data-test='ResultCardPrice']")

    flight_nights = flight_card_left.find_element(By.XPATH, value=".//div[contains(@class, 'ResultCardItinerarystyled__SectorLayoverTextBackground')]").text
    flight_nights_int = int(flight_nights.split(' ')[0])

    flight_price = flight_card_right.find_element(By.XPATH, value=".//strong[@data-test='ResultCardPrice']//span").text
    flight_price_int = int(flight_price.split(' ')[0])

    print(f"Nights: {flight_nights_int}, price: {flight_price_int}")

    if NIGHTS_SPENT_MIN <= flight_nights_int <= NIGHTS_SPENT_MAX and flight_price_int <= PRICE_LIMIT:
        print('Flight passed condition')
        nights_count.append(flight_nights_int)
        prices.append(flight_price)
        info = flight_card_left.find_elements(By.XPATH, value=".//div[contains(@class, 'ResultCardstyled__ResultCardSection')]")
        
        # Dates
        date_regex = './/p//time'
        departure_date = info[0].find_element(By.XPATH, value=date_regex).text
        departure_dates.append(departure_date)
        return_date = info[1].find_element(By.XPATH, value=date_regex).text
        return_dates.append(return_date)

        # Airports
        airports_xpath = ".//div[contains(@class, 'ResultCardItineraryPlacestyled__StyledResultCardItineraryPlace')]"
        departure_airports = info[0].find_elements(By.XPATH, value=airports_xpath)
        return_airports = info[1].find_elements(By.XPATH, value=airports_xpath)
        
        # Departure from info
        departure_from_time = departure_airports[0].find_element(By.TAG_NAME, value='time').text
        departure_from_city = departure_airports[0].find_element(By.TAG_NAME, value='span').text
        departure_from_airport = departure_airports[0].find_element(By.TAG_NAME, value='div').text
        departure_from_info.append(departure_from_time + ' ' + departure_from_city + ' ' + departure_from_airport)

        # Departure to info
        departure_to_time = departure_airports[1].find_element(By.TAG_NAME, value='time').text
        departure_to_city = departure_airports[1].find_element(By.TAG_NAME, value='span').text
        departure_to_airport = departure_airports[1].find_element(By.TAG_NAME, value='div').text
        departure_to_info.append(departure_to_time + ' ' + departure_to_city + ' ' + departure_to_airport)

        # Return from info
        return_from_time = return_airports[0].find_element(By.TAG_NAME, value='time').text
        return_from_city = return_airports[0].find_element(By.TAG_NAME, value='span').text
        return_from_airport = return_airports[0].find_element(By.TAG_NAME, value='div').text
        return_from_info.append(return_from_time + ' ' + return_from_city + ' ' + return_from_airport)

        # Return to info
        return_to_time = return_airports[1].find_element(By.TAG_NAME, value='time').text
        return_to_city = return_airports[1].find_element(By.TAG_NAME, value='span').text
        return_to_airport = return_airports[1].find_element(By.TAG_NAME, value='div').text
        return_to_info.append(return_to_time + ' ' + return_to_city + ' ' + return_to_airport)

        # Duration
        duration_xpath = '//div[@data-test="TripDurationBadge"]'
        departure_duration.append(info[0].find_element(By.XPATH, value=duration_xpath).text)
        return_duration.append(info[1].find_element(By.XPATH, value=duration_xpath).text)

        # Fly logo
        fly_logo_xpath = "//img[contains(@class, 'CarrierLogo__StyledImage-sc')]"
        departure_logo.append(info[0].find_element(By.XPATH, value=fly_logo_xpath).get_attribute("alt"))
        return_logo.append(info[1].find_element(By.XPATH, value=fly_logo_xpath).get_attribute("alt"))

def export_data_as_csv():
    df = pd.DataFrame({
        'Departure date': departure_dates, 
        'Return date': return_dates, 
        'Nights Count': nights_count, 
        'Departure from': departure_from_info, 
        'Departure to': departure_to_info, 
        'Departure air company': departure_logo,
        'Departure duration': departure_duration, 
        'Return from': return_from_info, 
        'Return to': return_to_info, 
        'Return air company': return_logo,
        'Return duration': return_duration,
        'Price': prices
    })

    df.to_csv('fligths-scraped.csv')
    print(df)

def main():
    # Initialize the driver
    driver = initialize_driver()
    website = 'https://www.kiwi.com/en/'
    driver.get(website)
    # driver.maximize_window()

    try:
        # Close the cookies dialog
        close_cookies_dialog(driver)

        # Set anywhere as destination input
        set_anywhere_as_destination_input(driver)

        # Navigate to results
        explore_url = get_explore_url(driver)
        driver.get(explore_url)
        print('Explore url opened')

        # Set eur as currency
        set_eur_as_currency(driver)

        # Set 1 cabin bag
        set_cabin_bag(driver)
        
        destination_links = get_destination_links(driver)
        destination_links_len = len(destination_links)

        wait = WebDriverWait(driver, 20)

        # Scroll to load more flights
        for index_destination, link in enumerate(destination_links):
            print(f"Checking destination: {index_destination + 1}/{destination_links_len}")
            
            # Open link
            driver.get(link)

            load_more(driver)

            try:
                flights = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-test='ResultCardWrapper']")))
                flights_len = len(flights)
                
            except exceptions.TimeoutException:
                print("No flights found.")
                continue
    
            for index, flight in enumerate(flights):
                print(f"Flights checked: {index + 1}/{flights_len}")
                try: 
                    flight_id = flight.find_element(By.XPATH, value=".//div[contains(@class, 'ResultCardstyled__ResultCardInner')]").get_attribute("data-test")
                    print(f"Flight id: {flight_id}")

                    if flight_id not in flights_ids:
                        print(f"Flight with id: {flight_id} is being processed")
                        flights_ids.append(flight_id)
                        check_flight_and_collect_if_conditions_are_met(flight)

                except exceptions.WebDriverException as e:
                    print(e)
                    pass

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        driver.quit()

        export_data_as_csv()
 
    except exceptions.StaleElementReferenceException as e: 
        print(e)
        pass

if __name__ == "__main__":
    main()