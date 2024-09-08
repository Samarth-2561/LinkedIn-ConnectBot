# LinkedIn ConnectBot

## Overview

LinkedIn ConnectBot is an automation tool designed to scrape company profiles from a list, enable notifications on their pages, and automatically send invitations to your connections. It helps manage your LinkedIn connections and interactions more efficiently by automating repetitive tasks.

## Features

- Scrapes company data from your list.
- Visits each company's LinkedIn page and enables notifications.
- Sends invitations to your LinkedIn connections automatically.
- Maintains a log of scrapped companies in `companies.csv`.
- Logs all connection invites in `connection_invites.csv`.

## How it Works

1. **Scrape Company List**: The bot fetches the list of companies from your provided list and scrapes data about each company.
2. **Enable Notifications**: It visits each company's LinkedIn page and enables notifications.
3. **Send Invitations**: It proceeds to invite your connections automatically to those companies.
4. **CSV Logging**: The bot stores a list of scrapped companies in `companies.csv` and invited connections in `connection_invites.csv` for tracking and auditing purposes.

## Installation

To set up and run the LinkedIn Bot Scrapper on your machine, follow the steps below:

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/linkedin-bot-scrapper.git
```

### 2. Navigate to the project directory

```
cd linkedin-bot-scrapper
```

### 3. Create a Python Virtual Environment:

```
python3 -m venv ./venv
```

### 4. Activate the Virtual Environment:

For Linux/macOS:

```
source ./venv/bin/activate
```

For Windows:

```
source ./venv/bin/activate
```

### 5. Install required dependencies:

```
pip install -r requirements.txt
```

### 6. Create .env file

Create a .env file and add your email under key 'EMAIL' and password under key 'PASSWORD'

```
EMAIL=<your_email>
PASSWORD=<your_password>
```

### 6. Run the Script

```
python main.py
```

## Usage

1. Update your company list in company_list.txt (or wherever you store the list of companies).
2. Run the LinkedIn ConnectBot:

```
python main.py
```

3. The bot will start scraping the company profiles, enabling notifications, and inviting connections. You can monitor the process through the terminal or log files.
4. The bot will generate two CSV files:<br>
   a. companies.csv: Lists all the companies scrapped. <br>
   b. connection_invites.csv: Lists all the connections invited.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
