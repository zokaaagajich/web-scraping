import audible_search_shared_methods as audible_shared
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def main():
    # Initialize the driver
    driver = audible_shared.initialize_driver()
    website = 'https://www.audible.com/search'
    driver.get(website)

    refinement_dropdwon_wait = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[@aria-labelledby='sortBy']")))
    refinement_dropdown = Select(refinement_dropdwon_wait)
    refinement_dropdown.select_by_value('popularity-rank')

    driver.quit()

if __name__ == "__main__":
    main()