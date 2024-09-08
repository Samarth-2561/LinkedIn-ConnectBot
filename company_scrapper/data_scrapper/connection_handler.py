from selenium.webdriver.common.by import By
import time
from loguru import logger
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

from .util.csv_writer import writeConnectionsToCSV

def inviteConnectionsToTheCompany(driver, connection_invited):
    try:
        logger.info("Attempting to invite connections to the company.")
        buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "artdeco-dropdown__trigger") and contains(@class, "org-overflow-menu__dropdown-trigger")]')

        # Click the overflow menu button
        for button in buttons:
            if '#overflow-web-ios-small' in button.get_attribute('innerHTML'):
                driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
                driver.implicitly_wait(3)
                found_invite_button = False
                # Find the invite connections button
                invite_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "org-overflow-menu__item")]')
                for invite_button in invite_buttons:
                    print(invite_button.get_attribute('innerHTML'))
                    if '#connect-medium' in invite_button.get_attribute('innerHTML'):
                        found_invite_button = True
                        invite_button.click()
                        logger.info("Clicked the invite connections button.")
                        time.sleep(5)
                        driver.implicitly_wait(5)

                        # Iterate over the first 50 checkboxes and invite connections
                        invited_people = 0
                        modal = driver.find_element(By.XPATH, '//*[@id="invitee-picker-results-container"]')
                        time.sleep(3)
                        driver.implicitly_wait(3)


                        while invited_people <= 1:
                            checkboxes = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')

                            for checkbox in checkboxes:
                                if 'checkbox-invitee-suggestion' in checkbox.get_attribute('outerHTML'):
                                    if not checkbox.is_selected():  # Check if the checkbox is not already selected
                                        if(invited_people > 1):
                                            break
                                        parent_checkbox_element = checkbox.find_element(By.XPATH, './..')

                                        # Locate the div containing the name and title
                                        name_element = parent_checkbox_element.find_element(By.XPATH, './/div[@class="t-16 t-black t-bold"]')
                                        title_element = parent_checkbox_element.find_element(By.XPATH, './/div[@class="t-14 t-black--light t-normal"]')

                                        person_name = name_element.text
                                        person_title = title_element.text

                                        # Ensure that the person hasn't already been invited
                                        if all(item['person_name'] != person_name and item['person_title'] != person_title for item in connection_invited):
                                            writeConnectionsToCSV([{
                                                'person_name': person_name,
                                                'person_title': person_title,
                                                'company_url': driver.current_url
                                            }])
                                            connection_invited.append({
                                                'person_name': person_name,
                                                'person_title': person_title,
                                                'company_url': driver.current_url
                                            })
                                            invited_people += 1
                                            driver.execute_script("arguments[0].click();", checkbox)
                                            logger.info(f"Invited {person_name}")

                            # Scroll the modal to load more suggestions
                            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)

                        time.sleep(2)

                        # Dismiss the modal after the invites
                        # dismiss_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "artdeco-button--circle") and contains(@class, "artdeco-modal__dismiss")]')
                        # for dismiss_button in dismiss_buttons:
                        #     if '#close-medium' in dismiss_button.get_attribute('outerHTML'):
                        #         driver.execute_script("arguments[0].click();", dismiss_button)
                        #         time.sleep(2)
                        #         try:
                        #             alert = driver.switch_to.alert
                        #             alert.accept()
                        #             logger.info("Closed the modal and accepted any alerts.")
                        #         except:
                        #             logger.info("No alert found to accept.")
                        #         break

                        invite_buttons = driver.find_elements(By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                        for invite_button in invite_buttons:
                            if('Invite' in invite_button.get_attribute('outerHTML') and 'Invite connections' not in invite_button.get_attribute('outerHTML')):
                                print(invite_button.get_attribute('outerHTML'))
                                # invite_button.click()
                                break
                
                if(found_invite_button == False): logger.warning("No Invite Button Found for Company")

    except NoSuchElementException as e:
        logger.error(f"Element not found while inviting connections: {e}")
    except TimeoutException as e:
        logger.error(f"Timeout occurred while inviting connections: {e}")
    except WebDriverException as e:
        logger.error(f"WebDriverException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
