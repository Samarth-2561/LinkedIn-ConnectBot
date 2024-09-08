from selenium.webdriver.common.by import By
from loguru import logger
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def clickTheFollowButton(driver, company_id):
    try:
        logger.info("Attempting to follow company with ID: {}", company_id)
        driver.implicitly_wait(5)  # Adjust the timeout according to your needs
        buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "artdeco-button--circle") and contains(@class, "artdeco-button--muted") and contains(@class, "artdeco-button--tertiary")]')
        
        if not buttons:
            logger.warning("No follow buttons found for company ID: {}", company_id)
            return

        for button in buttons:
            inner_html = button.get_attribute('innerHTML')
            if('#bell-fill-medium' in inner_html or '#bell-double-fill-medium' in inner_html):
                logger.debug("Found follow button for company ID: {}. Clicking...", company_id)
                driver.execute_script("arguments[0].click();", button)
                driver.implicitly_wait(3)
                time.sleep(3)

                try:
                    label = driver.find_element(By.XPATH, '//label[@for="id_ALL"]')
                    label.click()
                    logger.debug("Selected 'All' notifications for company ID: {}", company_id)

                    parent_div = driver.find_element(By.XPATH, '//div[contains(@class, "artdeco-modal__actionbar")]')
                    
                    # Find and click the confirmation button
                    button = parent_div.find_element(By.XPATH, './/button[contains(@class, "artdeco-button--primary")]')
                    button.click()
                    logger.info("Successfully set notifications for company ID: {}", company_id)
                    break
                except NoSuchElementException as e:
                    logger.error("Could not locate the necessary elements for setting notifications: {}", str(e))
                except TimeoutException as e:
                    logger.error("Timeout while setting notifications for company ID {}: {}", company_id, str(e))

        time.sleep(2)

    except WebDriverException as e:
        logger.error("WebDriverException occurred while following company {}: {}", company_id, str(e))
    except Exception as e:
        logger.error("Unexpected error occurred while following company {}: {}", company_id, str(e))

