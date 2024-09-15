from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .util.csv_writer import writeCompanyNewHires
from .extract_alumni import extractNotableAlumni

from loguru import logger

def extractNewHires(driver, company_id='upstart-network'):
    logger.info("Navigating to the LinkedIn insights page.")
    driver.get("https://www.linkedin.com/company/"+str(company_id)+"/insights/")
    company_name = driver.current_url.split("/")[4]
    data = []

    wait = WebDriverWait(driver, 10)
    logger.info("Waiting for the 'premium-insights-talent-change-card' section to load.")
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//section[@data-view-name='premium-insights-talent-change-card']"))
    )

    time.sleep(10)
    driver.implicitly_wait(10)
    
    # Locate the section and scroll into view
    try:
        section = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//section[@data-view-name='premium-insights-talent-change-card']")
        ))
        logger.info("Located the 'premium-insights-talent-change-card' section.")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        
        # Scroll to the section to bring it into view
        # driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", section)
        logger.info("Scrolled to the 'New Hires' section.")

    except Exception as e:
        logger.error("Failed to locate or scroll to the 'New Hires' section.")
        logger.error(f"Exception: {e}")
    
    logger.info("Locating the 'premium-insights-talent-change-card' section.")
    section = driver.find_element(By.XPATH, "//section[contains(@data-view-name, 'premium-insights-talent-change-card')]")

    # Within the section, find the carousel <ul>
    logger.info("Finding the carousel within the section.")
    carousel_ul = section.find_element(By.XPATH, ".//ul[contains(@class, 'artdeco-carousel__slider')]")

    while True:
        # Wait for the page to load
        time.sleep(2)
        driver.implicitly_wait(2)
        logger.info("Retrieving list items from the carousel.")
        li_elements = carousel_ul.find_elements(By.XPATH, "./li[div[@data-test-display='display']]")

        if not li_elements:
            logger.warning("No list items found in the carousel.")
            break

        for li in li_elements:
            try:
                name = li.find_element(By.XPATH, ".//span[contains(@class, 'org-senior-hire-card__hire-name')]").text.strip()
            except Exception as e:
                name = ''

            try:
                title = li.find_element(By.XPATH, ".//p[contains(@class, 'org-senior-hire-card__hire-title')]").text.strip()
            except Exception as e:
                title = ''

            try:
                date = li.find_element(By.XPATH, ".//p[contains(@class, 't-black--light') and not(contains(@class, 'org-senior-hire-card__hire-title'))]").text.strip()
            except Exception as e:
                date = ''

            try:
                profile_url = li.find_element(By.XPATH, ".//a[contains(@class, 'org-senior-hire-card__link')]").get_attribute('href')
            except Exception as e:
                profile_url = ''

            if title == '' and date == '':
                logger.warning("Both title and date are empty, skipping this entry.")
                continue

            entry = {
                'name': name,
                'title': title,
                'date': date,
                'profile_url': profile_url,
                'company_name': company_name
            }
            data.append(entry)
            logger.info(f"Extracted data: Name: {name}, Title: {title}, Date: {date}, Profile URL: {profile_url}, Company Name: {company_name}")

        # Try to click the Next button if it's enabled
        try:
            logger.info("Attempting to click the 'Next' button.")
            next_button = section.find_element(By.XPATH, ".//button[contains(@class, 'artdeco-pagination__button--next') and not(@disabled)]")
            driver.execute_script("arguments[0].click();", next_button)
            logger.info("'Next' button clicked, moving to the next page.")
        except Exception as e:
            # Next button not found or not clickable
            logger.info("Next button is disabled or not found. Ending extraction.")
            break
    
    writeCompanyNewHires(company_name=company_name, new_hires_data=data)

    logger.info(f"New Hires data extracted and written to csv for company {company_name}. No of New Hires Extracted: {len(data)}")

    extractNotableAlumni(driver=driver, company_name=company_name)
    
    return data
