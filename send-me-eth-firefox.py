from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from random import randint
from time import sleep
import os
import json
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime


# load environment variables from .env file
load_dotenv()
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
WALLET_ADDRESSES = json.loads(os.getenv('WALLET_ADDRESSES'))
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')

# setup FireFox Driver with options

s = Service(GeckoDriverManager().install())
op = webdriver.FirefoxOptions()
op.add_argument('--headless')  # set headless mode - the browser won't show
op.add_argument('--window-size=1920,1080')  # set the browser size 1920,1080
#op.add_experimental_option("excludeSwitches", ["enable-automation"])
#op.add_experimental_option('useAutomationExtension', False)

# user_agent must be specified for headless mode to avoid reCAPTCHA check
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
op.add_argument(f'user-agent={user_agent}')
driver = webdriver.Firefox(service=s, options=op)

multi_addresses = False  # Change to True if using multiple addresses
time_log = []

if multi_addresses:  # multiple addresses
    for i, address in enumerate(WALLET_ADDRESSES):
        # enter the wallet address
        driver.get("https://www.rinkebyfaucet.com/")
        sleep(randint(5, 15))  # sleep random 5-15 seconds 
        #driver.find_element(By.CLASS_NAME, "alchemy-faucet-panel-input-text").clear()
        driver.find_element(By.CLASS_NAME, "alchemy-faucet-panel-input-text").send_keys(address)
        sleep(randint(5, 15))  # sleep random 5-15 seconds 

        # find the button and click
        search_button = driver.find_element(By.CLASS_NAME, 'alchemy-faucet-button')
        search_button.click()
        sleep(randint(3, 10))  # sleep random 3-10 seconds

        # make a screenshot for debugging
        # driver.get_screenshot_as_file(f'screenshot{i}.png')
        time_log.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(f'tried #{i+1} address: {address}')
        sleep(randint(20, 60))  # pause random 20-60 seconds before each request

else:
    driver.get("https://www.rinkebyfaucet.com/")
    sleep(randint(5, 15))  # sleep random 5-15 seconds 
    # enter the wallet address
    #driver.find_element(By.CLASS_NAME, "alchemy-faucet-panel-input-text").clear()
    driver.find_element(By.CLASS_NAME, "alchemy-faucet-panel-input-text").send_keys(WALLET_ADDRESS)
    sleep(randint(5, 15))  # sleep random 5-15 seconds 

    # find the button and click
    search_button = driver.find_element(By.CLASS_NAME, 'alchemy-faucet-button')
    search_button.click()
    
    print(f'tried 1 address: {WALLET_ADDRESS}')
    sleep(randint(2, 5))
    #driver.get_screenshot_as_file(f'screenshot.png')

# send an email after each try
message = Mail(
    from_email=FROM_EMAIL,
    to_emails=TO_EMAIL,
    subject='Getting More Eth',
    html_content='<p>Tried to get Eth at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p> <p>Time log: ' + str(time_log) + '</p>')
try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

driver.close()
