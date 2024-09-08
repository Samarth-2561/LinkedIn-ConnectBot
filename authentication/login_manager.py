
import pandas as pd
from loguru import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
import os
import time
import pickle
from selenium.webdriver.common.keys import Keys

def loginUserUsingPassword(driver):
    try:
        logger.info("Attempting to log in using username and password.")
        
        # Locate the username field and enter the email
        try:
            username = driver.find_element(By.ID, "username")
            username.send_keys(os.getenv('EMAIL'))
            logger.debug("Entered the username.")
        except NoSuchElementException as e:
            logger.error("Username field not found. Error: {}", e)
            return False

        # Locate the password field and enter the password
        try:
            password = driver.find_element(By.ID, "password")
            password.send_keys(os.getenv('PASSWORD'))
            logger.debug("Entered the password.")
        except NoSuchElementException as e:
            logger.error("Password field not found. Error: {}", e)
            return False

        # Submit the login form
        password.send_keys(Keys.RETURN)

        # Allow some time for the login process
        time.sleep(5)

        # Check if login was successful by verifying the URL
        if driver.current_url != "https://www.linkedin.com/feed/":
            logger.warning("Login not successful, possibly due to 2FA. Waiting for manual 2FA input.")
            # Pause to allow for manual 2FA code entry
            while('challenge' in driver.current_url):
                logger.warning("2FA required, Waiting for manual 2FA input..")
                time.sleep(15)

        # After successful login, navigate to network manager and store cookies
        driver.get("https://www.linkedin.com/mynetwork/network-manager/company/")
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        logger.success("Login successful. Cookies stored for future use.")
        return True

    except Exception as e:
        logger.error("An unexpected error occurred while logging in: {}", e)
        return False

