
import pickle
from loguru import logger
from selenium.common.exceptions import WebDriverException
import time

def setCookiesAndCheckIfCookiesAreValid(driver):
    try:
        logger.info("Navigating to LinkedIn login page to set cookies.")
        driver.get("https://www.linkedin.com/login")

        # Load cookies from the pickle file
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            logger.info("Cookies loaded successfully from cookies.pkl.")
        except FileNotFoundError as e:
            logger.error("cookies.pkl file not found. Ensure the cookies file exists. Error: {}", e)
            return False
        except Exception as e:
            logger.error("An error occurred while loading cookies from cookies.pkl: {}", e)
            return False

        # Add cookies to the browser
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except WebDriverException as e:
                logger.error("Failed to add cookie: {}. Error: {}", cookie, e)

        # Navigate to the network manager page to verify if the cookies are valid
        driver.get("https://www.linkedin.com/mynetwork/network-manager/company/")
        time.sleep(2)

        # Check if we successfully reached the expected URL
        if driver.current_url != "https://www.linkedin.com/mynetwork/network-manager/company/":
            logger.warning("Cookies are invalid or session expired. Redirected to a different URL.")
            return False
        else:
            logger.info("Cookies are valid, successfully navigated to the network manager page.")
            return True
    
    except Exception as e:
        logger.error("An unexpected error occurred: {}", e)
        return False
