import requests
from bs4 import BeautifulSoup

# Fetch HTML
website = 'https://www.kiwi.com/en/search/results/belgrade-serbia/paris-france'
try: 
    response = requests.get(website) 
except requests.exceptions.RequestException as err:
    print("Error fetching page")
    exit()    
content = response.text

# Parse HTML
soup = BeautifulSoup(content, 'lxml')

print(soup)
print(soup.find_all('a'))
print(soup.get_text())