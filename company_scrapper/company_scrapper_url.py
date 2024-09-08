from loguru import logger
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By


def getUniqueCompaniesIdsForScrapping(driver, company_parsed_data, companies_to_load=10):
    try:
        logger.info("Starting company ID scraping process with target of loading {} companies.", companies_to_load)
        companies_loaded = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        logger.debug("Initial scroll height: {}", last_height)
        company_links = []
        final_company_links = []
        time.sleep(2)
        scroll_counter = 0

        while companies_loaded < companies_to_load and scroll_counter < 2:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                time.sleep(5)
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scroll_counter+=1
                    logger.info("Reached the bottom of the page. No more content to load.")

                last_height = new_height

                # Count the number of companies loaded so far
                company_links = driver.find_elements(By.CSS_SELECTOR, "a.app-aware-link")
                logger.debug("Found {} company links on the page.", len(company_links))
                for link in company_links:
                    href = link.get_attribute("href")
                    if "/company/" in href:
                        company_id = href.split("/company/")[1].split("/")[0]
                        if any(item['company_id'] == int(company_id) for item in company_parsed_data) == False:
                            final_company_links.append(link)

                companies_loaded = len(final_company_links)
                logger.info("{} companies loaded so far.", companies_loaded)

            except NoSuchElementException as e:
                logger.error("Error finding company links: {}", str(e))
            except TimeoutException as e:
                logger.error("Page load timeout: {}", str(e))

        logger.info("Finished scrolling. Now extracting unique company IDs.")
        
        # Extract the company IDs from the final company links
        company_links = final_company_links  
        unique_company_ids = []
        for link in company_links:
            href = link.get_attribute("href")
            if "/company/" in href:
                company_id = href.split("/company/")[1].split("/")[0]
                if company_id not in unique_company_ids:  # Avoid duplicates while preserving order
                    unique_company_ids.append(company_id)
                    logger.debug("Unique company ID {} extracted.", company_id)
                    if(len(unique_company_ids) == 10):
                        break
        
        logger.info("Total unique company IDs extracted: {}", len(unique_company_ids))
        return unique_company_ids 

    except Exception as e:
        logger.error("An unexpected error occurred: {}", str(e))
        raise