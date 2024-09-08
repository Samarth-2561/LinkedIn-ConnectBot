
from util.driver_manager import init_driver, quit_driver
from authentication.cookie_manager import setCookiesAndCheckIfCookiesAreValid
from dotenv import load_dotenv
import os
from loguru import logger
from authentication.login_manager import loginUserUsingPassword
from util.csv_creater import createCompaniesCSVFile, createConnectionInvitesCSVFile
import pandas as pd
from company_scrapper import getUniqueCompaniesIdsForScrapping
import time
from company_scrapper import extractCompaniesData

def main():
    load_dotenv()
    
    driver = init_driver()
    
    try:
        validCookies = setCookiesAndCheckIfCookiesAreValid(driver=driver)
        if(validCookies):
            logger.success("Cookies are Valid, Skipping the Login")
        if(validCookies == False):
            logger.success("Cookies are Invalid, trying login now")
            loginUserUsingPassword(driver)
            # Add more automation logic here if needed
        
        createCompaniesCSVFile()
        createConnectionInvitesCSVFile()

        company_parsed_data_df = pd.read_csv('./documents/companies.csv')

        company_parsed_data = company_parsed_data_df.to_dict(orient='records')

        connection_invited_df = pd.read_csv('./documents/connection_invites.csv')

        connection_invited = connection_invited_df.to_dict(orient='records')

        logger.info("Starting the Scrapping Process")

        company_ids = getUniqueCompaniesIdsForScrapping(driver=driver, company_parsed_data=company_parsed_data)
        
        extractCompaniesData(driver=driver, company_ids=company_ids, company_parsed_data=company_parsed_data, connection_invited=connection_invited)

        time.sleep(500)
    except Exception as e:
        print(e)
    finally:
        quit_driver(driver)

if __name__ == "__main__":
    main()
