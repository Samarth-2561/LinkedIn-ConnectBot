
from selenium import webdriver
from loguru import logger

def init_driver():
    try:
        logger.info("Initializing the Chrome WebDriver.")
        driver = webdriver.Chrome()
        return driver
    except Exception as e:
        logger.error("Failed to initialize WebDriver: {}", str(e))
        raise

def quit_driver(driver):
    try:
        logger.info("Closing the WebDriver.")
        driver.quit()
    except Exception as e:
        logger.error("Failed to close WebDriver: {}", str(e))
        raise
