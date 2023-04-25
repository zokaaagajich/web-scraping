from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

website = 'https://www.kiwi.com/en/search/results/belgrade-serbia/malaga-spain'
path = '/usr/local/bin/chromedriver_mac64/chromedriver'
service = Service(executable_path=path) 
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

driver.quit() 