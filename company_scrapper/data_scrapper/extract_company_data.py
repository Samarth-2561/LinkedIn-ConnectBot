import time
from loguru import logger
from .util.csv_writer import writeCompanyDataToCSV
from selenium.common.exceptions import NoSuchElementException
from .follower_handler import clickTheFollowButton
from selenium.webdriver.common.by import By

from .connection_handler import inviteConnectionsToTheCompany
from .extract_new_hires import extractNewHires


def has_connection(driver):
    try:
        logger.info("Checking if connection exists.")
        driver.find_element(By.XPATH, '//span[@jsselect="heading" and @jsvalues=".innerHTML:msg"]')
        logger.info("No connection found.")
        return False
    except NoSuchElementException:
        logger.info("Connection Successful.")
        return True
    except Exception as e:
        logger.error(f"An unexpected error occurred while checking for connection: {e}")


def extractCompaniesData(driver, company_ids, company_parsed_data, connection_invited):
    for company_id in company_ids:
        try:
            posts_url = f"https://www.linkedin.com/company/{company_id}/posts/?feedView=all"
            logger.info(f"Visiting: {posts_url}")
            driver.get(posts_url)
            while(has_connection(driver=driver) == False):
                time.sleep(10)
                driver.implicitly_wait(10)

            
            # Allow time to load the posts page
            time.sleep(5)  # Adjust as needed
            logger.debug(f"Page loaded for company ID: {company_id}")
            
            # Step 1: Click the bell icon and set notifications to "All"
            try:
                logger.info(f"Attempting to follow company and set notifications for company ID: {company_id}")
                clickTheFollowButton(driver=driver, company_id=company_id)
            except Exception as e:
                logger.error(f"Failed to follow or set notifications for company ID {company_id}: {e}")

            # Step 2: Click the 3 dots and invite the specific friend (Functionality to be added)
            # try:
            #     inviteConnectionsToTheCompany(driver=driver, connection_invited=connection_invited)
            # except Exception as e:
            #     logger.error(f"Failed to invite connections for company ID {company_id}: {e}")
            #     raise

            
            # Step 3: Extract Data from Insights
            try:
                logger.info(f"Attempting to extract insights for company ID: {company_id}")
                extractNewHires(driver=driver, company_id=company_id)
            except Exception as e:
                logger.error(f"Failed to follow or set notifications for company ID {company_id}: {e}")
            
            # Prepare the payload and write to CSV
            company_payload = {
                'company_id': company_id,
                'company_url': posts_url
            }
            logger.info(f"Writing company data to CSV for company ID: {company_id}")
            writeCompanyDataToCSV([company_payload])
            company_parsed_data.append(company_payload)
            logger.info(f"Successfully parsed and saved data for company ID: {company_id}")            
        except Exception as e:
            logger.error(f"Unexpected error while processing company ID {company_id}: {e}")
