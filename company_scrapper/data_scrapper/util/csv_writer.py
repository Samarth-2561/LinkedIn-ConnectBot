
import pandas as pd
from loguru import logger

def writeCompanyDataToCSV(company_data):
    try:
        pd.DataFrame(company_data).to_csv("./documents/companies.csv", mode='a', header=False, index=False)
        logger.info("Successfully wrote company data for ID: {}", company_data[0]['company_id'])
    except PermissionError as e:
        logger.error("Permission denied: unable to write to companies.csv. Make sure the file is not open elsewhere. Error: {}", str(e))
    except Exception as e:
        logger.error("Unexpected error occurred while writing company data to CSV: {}", str(e))
        raise

def writeConnectionsToCSV(connection_invites):
    try:
        pd.DataFrame(connection_invites).to_csv("./documents/connection_invites.csv", mode='a', header=False, index=False)
        logger.info("Successfully appended connection invites to {} for Company ID {}", connection_invites[0]['person_name'], connection_invites[0]['company_url'])
    except PermissionError as e:
        logger.error("Permission denied: Unable to write to connection_invites.csv. Ensure the file is not open elsewhere. Error: {}", str(e))
    except Exception as e:
        logger.error("Unexpected error occurred while writing connection invites to CSV: {}", str(e))
        raise
