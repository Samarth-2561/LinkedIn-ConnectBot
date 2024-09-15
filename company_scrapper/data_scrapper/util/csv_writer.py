
import pandas as pd
from loguru import logger
import os

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

def createCompanyDataFolder():
    if not os.path.exists("documents/new_hires"):
        os.makedirs("documents/new_hires")
        logger.info(f"Directory new_hires  created.")
    else:
        logger.info(f"Directory new_hires already exists.")

    if not os.path.exists("documents/notable_alumni"):
        os.makedirs("documents/notable_alumni")
        logger.info(f"Directory notable_alumni  created.")
    else:
        logger.info(f"Directory notable_alumni already exists.")


def writeCompanyNewHires(company_name, new_hires_data):
    createCompanyDataFolder()
    try:
        pd.DataFrame(new_hires_data).to_csv(f"./documents/new_hires/{company_name}.csv", mode='w', header=True, index=False)
        logger.info(f"Successfully created the new_hires.csv for {company_name}")
    except PermissionError as e:
        logger.error("Permission denied: Unable to write to new_hires.csv. Ensure the file is not open elsewhere. Error: {}", str(e))
    except Exception as e:
        logger.error("Unexpected error occurred while writing new hires to CSV: {}", str(e))
        raise

def writeCompanyNotableAlumni(company_name, notable_alumni_data):
    createCompanyDataFolder()
    try:
        pd.DataFrame(notable_alumni_data).to_csv(f"./documents/notable_alumni/{company_name}.csv", mode='w', header=True, index=False)
        logger.info(f"Successfully created the notable_alumni.csv for {company_name}")
    except PermissionError as e:
        logger.error("Permission denied: Unable to write to not.csv. Ensure the file is not open elsewhere. Error: {}", str(e))
    except Exception as e:
        logger.error("Unexpected error occurred while writing new hires to CSV: {}", str(e))
        raise