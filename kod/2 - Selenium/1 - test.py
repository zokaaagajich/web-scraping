import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

website = 'https://www.kiwi.com/en/'
path = '/usr/local/bin/chromedriver_mac64_arm64/chromedriver'
service = Service(executable_path=path) 
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

try:
    # Close cookies dialog
    cookie_dialog_close_btn = driver.find_element(By.XPATH, value=".//section[@id='cookie_consent']//button[@aria-label='Close']")
    cookie_dialog_close_btn.click()

    time.sleep(10)

    print(driver.page_source)   
    
    driver.quit()

except exceptions.StaleElementReferenceException as e: 
    print(e)
    pass