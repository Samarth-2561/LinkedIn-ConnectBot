from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from loguru import logger
from .util.csv_writer import writeCompanyNotableAlumni

def extractNotableAlumni(driver, company_name='upstart-network'):
    data = []

    time.sleep(4)
    driver.implicitly_wait(4)

    wait = WebDriverWait(driver, 10)

    logger.info("Waiting for the 'premium-insights-notable-alumni-card' section to load.")
    logger.info("Locating the 'premium-insights-notable-alumni-card' section.")
    try:
        section = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'org-notable-alumni-module')]")
        ))
        logger.info("Located the 'premium-insights-notable-alumni-card' section.")

        # Scroll to the section to bring it into view
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", section)
        logger.info("Scrolled to the 'Notable Alumni' section.")

    except Exception as e:
        logger.error("Failed to locate or scroll to the 'Notable Alumni' section.")
        logger.error(f"Exception: {e}")
    section = driver.find_element(By.XPATH, "//div[contains(@class, 'org-notable-alumni-module')]")

    # Within the section, find the carousel <ul>
    logger.info("Finding the carousel within the section.")
    carousel_ul = section.find_element(By.XPATH, ".//ul[contains(@class, 'artdeco-carousel__slider')]")

    while True:
        # Wait for the page to load
        time.sleep(3)
        driver.implicitly_wait(3)
        logger.info("Retrieving list items from the carousel.")
        li_elements = carousel_ul.find_elements(By.XPATH, "./li[div[@data-test-display='display']]")

        if not li_elements:
            logger.warning("No list items found in the carousel.")
            break

        for li in li_elements:
            try:
                name = li.find_element(By.XPATH, ".//a[contains(@class, 'org-notable-alumni-card__alumni-name')]").text.strip()
            except Exception as e:
                name = ''

            try:
                # Current position
                current_position = li.find_element(
                    By.XPATH,
                    ".//div[contains(@class, 'org-notable-alumni-card__current-alumni-detail')]//p[contains(@class, 'org-notable-alumni-card__alumni-title')]"
                ).text.strip()
            except Exception as e:
                current_position = ''

            try:
                # Previous position
                previous_position = li.find_element(
                    By.XPATH,
                    ".//div[contains(@class, 'org-notable-alumni-card__previous-alumni-detail')]//p[contains(@class, 'org-notable-alumni-card__alumni-title')]"
                ).text.strip()
            except Exception as e:
                previous_position = ''

            try:
                profile_url = li.find_element(By.XPATH, ".//a[contains(@class, 'org-notable-alumni-card__alumni-name')]").get_attribute('href')
            except Exception as e:
                profile_url = ''

            if(name == '' and current_position == '' and previous_position == ''):
                continue

            logger.info(f"Extracted data: Name: {name}, Current Position: {current_position}, Previous Position: {previous_position}, Profile URL: {profile_url}, Company Name: {company_name}")
            
            # Log the extracted information in a human-readable format
            # Append the extracted data to the list
            entry = {
                'name': name,
                'current_position': current_position,
                'previous_position': previous_position,
                'profile_url': profile_url,
                'company_name': company_name
            }
            data.append(entry)

        # Try to click the Next button if it's enabled
        try:
            logger.info("Attempting to click the 'Next' button.")
            next_button = section.find_element(By.XPATH, ".//button[contains(@class, 'artdeco-pagination__button--next') and not(@disabled)]")
            driver.execute_script("arguments[0].click();", next_button)
            logger.info("'Next' button clicked, moving to the next set of alumni.")
        except Exception as e:
            # Next button not found or not clickable
            logger.info("Next button is disabled or not found. Ending extraction.")
            break

    writeCompanyNotableAlumni(company_name=company_name, notable_alumni_data=data)

    logger.info(f"Notable Alumni data extracted and written to csv for company {company_name}. No of Notable Alumni Extracted: {len(data)}")

    return data
