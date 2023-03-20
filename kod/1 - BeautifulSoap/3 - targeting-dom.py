import re

import pandas as pd
from bs4 import BeautifulSoup

with open('flights-belgrade-malaga-page-source.txt', 'r') as file:
    soup = BeautifulSoup(file, 'lxml')
    
    all_flights = soup.find_all('div', class_="ResultCardstyled__ResultCardInner-sc-vsw8q3-9 hlQpUC") 

    departure_date_regex = re.compile('.*DepartureDate.*')
    departure_info_regex = re.compile('.*ResultCardItineraryPlacestyled__StyledResultCardItineraryPlace.*')

    flights = []
    departure_dates = []
    departure_info = []
    return_dates = []
    return_info = []
    nights = []
    prices = []

    for flight in all_flights:
        nights_spent = flight.find('div', class_='ResultCardItinerarystyled__SectorLayoverTextBackground-sc-iwhyue-8 cYplWP').text.split(' ')[0]
        
        dates = flight.find_all("p", {"class" : departure_date_regex})
        
        departure_dates.append(dates[0].find('time').text)
        return_dates.append(dates[1].find('time').text)    

        departure_time = flight.find_all('div',  {"class" : departure_info_regex})[0].find('time').text
        departure_airport = flight.find_all('div',  {"class" : departure_info_regex})[0].find('div').text
        departure_info.append(departure_time + ' ' + departure_airport)


        return_time = flight.find_all('div',  {"class" : departure_info_regex})[2].find('time').text
        return_airport = flight.find_all('div',  {"class" : departure_info_regex})[2].find('div').text
        return_info.append(return_time + ' ' + return_airport)

        nights.append(nights_spent)
        prices.append(flight.find('strong',  {"data-test" : 'ResultCardPrice'}).text)


    df_flights = pd.DataFrame({'Departure date': departure_dates, 'Departure info': departure_info, 'Return date': return_dates, 'Return info': return_info, 'Nights' : nights, 'Prices': prices})
    df_flights.to_csv('flights-belgrade-malaga-results.csv', index=False)