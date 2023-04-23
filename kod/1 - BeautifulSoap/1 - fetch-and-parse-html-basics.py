import requests
from bs4 import BeautifulSoup

# Fetch HTML
url = 'https://www.kiwi.com/en/search/results/belgrade-serbia/paris-france'
try: 
    response = requests.get(url) 
except requests.exceptions.RequestException as err:
    print("Error fetching page")
    exit()    
html = response.text

# Parse HTML
soup = BeautifulSoup(html, 'lxml')

print(soup)
print(soup.find_all('a'))
print(soup.get_text())