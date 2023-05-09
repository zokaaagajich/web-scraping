import random
import time

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

start_time = time.time()

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

website = 'https://www.kiwi.com/en/'
path = '/usr/local/bin/chromedriver_mac64_arm64/chromedriver'
service = Service(executable_path=path) 
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
# driver.maximize_window()

try:
    # Close cookies dialog
    time.sleep(10)
    cookie_dialog_close_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//section[@id='cookie_consent']//button[@aria-label='Close']")))
    cookie_dialog_close_btn.click()
    print('Cookies dialog closed')

    # Reach destination input and click on it
    destination_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-test='SearchPlaceField-destination']//input")))
    destination_input.click()

    # Catch anywhere option within dropdown and click on it
    time.sleep(10)
    anywhere_dropdown_option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-test='AnywhereRow']")))
    anywhere_dropdown_option.click()
    print('Anywhere added to destination input')

    # Get url from Explore btn
    time.sleep(10)
    explore_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@data-test='LandingSearchButton']"))).get_attribute('href')

    # Navigate to results
    driver.get(explore_url)
    print('Explore url opened')

    # Open currency settings (dialog)
    time.sleep(10)
    currency_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='RegionalSettingsButton']")))
    currency_btn.click()

    # # Choose currency within dropdown
    time.sleep(10)
    currency_dropdown_wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@data-test='CurrencySelect']")))
    currency_dropdown = Select(currency_dropdown_wait)
    currency_dropdown.select_by_value('eur')

    # Save currency
    save_currency_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='SubmitRegionalSettingsButton']")))
    save_currency_btn.click()
    print('Currency updated')

    # # Change sort
    # time.sleep(20)
    # sort_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-test='SortingButton']//button")))
    # sort_btn.click()

    # # Choose Cheepest option
    # time.sleep(10)
    # sort_by_price = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//tr[@data-test='SortBy-price']")))
    # sort_by_price.click()
    # print('Sort updated')

    # Choose 1 cabin bag
    time.sleep(10)
    bags = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test='SearchFormFilters-button-bags']")))
    bags.click()

    time.sleep(10)
    cabin_bag_increment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='increment']")))
    cabin_bag_increment.click()
    bags.click()
    print('Bags count updated')

    time.sleep(10)
    limit = 150
    destination_links = []
    destination_wrappers = driver.find_elements(By.XPATH, value="//a[@data-test='PictureCard']")
    for destination in destination_wrappers:
        price_unparsed = destination.find_element(By.XPATH, value='.//h3/span/span[2]')
        price = int(price_unparsed.text.split(' ')[0])

        if price <= limit:
            destination_links.append(destination.get_attribute('href'))

    print('Destination links: ', destination_links)

    departure_dates = []
    departure_from_info = []
    departure_to_info = []
    departure_duration = []

    return_dates = []
    return_from_info = []
    return_to_info = []
    return_duration = []

    nights_count = []
    prices = []

    destination_links_len = len(destination_links)

    for index_destination, link in enumerate(destination_links):
        driver.get(link)
        time.sleep(10)
        print('Checking destination: ', {index_destination + 1}/{destination_links_len})

        load_more_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ButtonPrimitiveContentChildren') and contains(text(), 'Load more')]")))
        load_more_btn.click()
        print('Loaded more')

        time.sleep(10)
        flights = driver.find_elements(By.XPATH, value="//div[@data-test='ResultCardWrapper']")
        flights_len = len(flights)
        nigths_min = 3
        nights_max = 6

        for index, flight in enumerate(flights):
            print(f"Flights checked: {index + 1}/{flights_len}")

            flight_card_left = flight.find_element(By.XPATH, value=".//div[contains(@class, 'ResultCardstyled__ResultCardMain')]")
            flight_card_right = flight.find_element(By.XPATH, value=".//div[@data-test='ResultCardPrice']")
            
            flight_nights = flight_card_left.find_element(By.XPATH, value=".//div[contains(@class, 'ResultCardItinerarystyled__SectorLayoverTextBackground')]").text
            flight_nights_int = int(flight_nights.split(' ')[0])

            flight_price = flight_card_right.find_element(By.XPATH, value=".//strong[@data-test='ResultCardPrice']//span").text
            flight_price_int = int(flight_price.split(' ')[0])

            if nigths_min <= flight_nights_int & flight_nights_int <= nights_max & flight_price_int <= limit:
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

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    
    driver.quit()
    
    df = pd.DataFrame({
        'Departure date': departure_dates, 
        'Return date': return_dates, 
        'Nights Count': nights_count, 
        'Departure from': departure_from_info, 
        'Departure to': departure_to_info, 
        'Departure duration': departure_duration, 
        'Return from': return_from_info, 
        'Return to': return_to_info, 
        'Return duration': return_duration,
        'Price': prices
    })

    df.to_csv('fligths-scraped.csv')
    print(df)

    
except exceptions.StaleElementReferenceException as e: 
    print(e)
    pass