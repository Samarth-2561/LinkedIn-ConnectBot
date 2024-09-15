import os
from loguru import logger
import csv

def createCompaniesCSVFile():
    try:
        if not os.path.exists("documents"):
            os.makedirs("documents")
            logger.info(f"Directory documents  created.")
        else:
            logger.info(f"Directory documents already exists.")

        if not os.path.exists('./documents/companies.csv'):
            logger.info("Creating companies.csv file with headers.")
            column_headers = ['company_id', 'company_url']
            with open('./documents/companies.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(column_headers)
            logger.info("companies.csv file created successfully.")
        else:
            logger.info("companies.csv file already exists. No action needed.")
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating companies.csv: {e}")
        raise

def createConnectionInvitesCSVFile():
    try:
        if not os.path.exists('./documents/connection_invites.csv'):
            logger.info("Creating connection_invites.csv file with headers.")
            column_headers = ['person_name', 'person_title', 'company_url']
            with open('./documents/connection_invites.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(column_headers)
            logger.info("connection_invites.csv file created successfully.")
        else:
            logger.info("connection_invites.csv file already exists. No action needed.")
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating connection_invites.csv: {e}")
        raise