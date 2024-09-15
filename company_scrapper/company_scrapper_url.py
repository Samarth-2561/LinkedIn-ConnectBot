from loguru import logger
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

def clickMoreResultButton(driver):
    show_more_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'scaffold-finite-scroll__load-button')]")
    for button in show_more_button:
        if 'Show more results' in button.get_attribute('innerHTML'):
            driver.execute_script("arguments[0].click();", button)
            break


def getUniqueCompaniesIdsForScrapping(driver, company_parsed_data, companies_to_load):
    try:
        logger.info("Starting company ID scraping process with target of loading {} companies.", companies_to_load)
        last_height = driver.execute_script("return document.body.scrollHeight")
        logger.debug("Initial scroll height: {}", last_height)
        time.sleep(2)
        scroll_counter = 0
        unique_company_ids = []  # Moved outside the while loop

        while len(unique_company_ids) < companies_to_load and scroll_counter < 10:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                driver.implicitly_wait(5)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scroll_counter += 1
                    logger.info("Reached the bottom of the page. No more content to load.")
                else:
                    scroll_counter = 0  # Reset scroll counter if new content is loaded

                clickMoreResultButton(driver)
                last_height = new_height
                company_links = driver.find_elements(By.CSS_SELECTOR, "a.app-aware-link")
                logger.debug("Found {} company links on the page.", len(company_links))

                for link in company_links:
                    href = link.get_attribute("href")
                    if "/company/" in href:
                        company_id = href.split("/company/")[1].split("/")[0]
                        if any(item['company_id'] == int(company_id) for item in company_parsed_data) == False:
                            if company_id not in unique_company_ids:  # Avoid duplicates
                                unique_company_ids.append(company_id)
                                logger.debug("Unique company ID {} extracted.", company_id)
                                if len(unique_company_ids) == companies_to_load:
                                    break

                logger.info("{} companies loaded so far.", len(unique_company_ids))

            except NoSuchElementException as e:
                logger.error("Error finding company links: {}", str(e))
            except TimeoutException as e:
                logger.error("Page load timeout: {}", str(e))

        logger.info("Finished scrolling. Now extracting unique company IDs. {} {}",len(unique_company_ids), companies_to_load)
        return unique_company_ids

    except Exception as e:
        logger.error("An unexpected error occurred: {}", str(e))
        return []
