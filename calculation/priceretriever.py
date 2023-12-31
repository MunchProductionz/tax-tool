import os
import requests
import json
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
import pandas as pd
from variables import fiat_currencies_full_names
from variables import cryptocurrencies_full_names
from variables import days_in_months
from variables import convert_values_to_lowercase
from variables import isValidCurrency
from variables import isUSDollar
from variables import isFiat

def get_average_USD_price_crypto_locally(date, ticker):

    with open(f'coin_data/coins_market_data.json', "r") as f:
        data = json.load(f)
        average_price = data[ticker][date]["current_price"]
    
    # print("Got average USD price of " + ticker + " on " + date + " from local storage")
    
    return average_price

def get_average_USD_price_crypto_API(date, ticker):
    
    # Get CoinGecko API key
    load_dotenv()
    api_key = os.environ["COINGECKO_API_KEY"]
    
    # Get the id of the currency
    supported_coins = get_supported_coins()
    currency = cryptocurrencies_full_names[ticker]
    currency_id = supported_coins[currency]
    
    # Format date
    formatted_date = get_formatted_date(date)
    
    # Send a GET request
    # - Use /coins/{id}/history endpoint
    # - Date format: dd-mm-yyyy
    url = "https://api.coingecko.com/api/v3/coins/" + currency_id + "/history?date=" + formatted_date + "&x_cg_demo_api_key=" + api_key
    response = requests.get(url)
    response_json = json.loads(response.text)
    average_price = response_json["market_data"]["current_price"]["usd"]
    
    # with open(f'coin_data/{currency}_historical_data_{date}.json', 'w') as outfile:
    #     outfile.write(json.dumps(response_json, indent=4))
    
    return average_price

def get_fiat_to_USD_conversion_rate(date, fiat):
    
    # Get fiat currency
    fiat_currency = fiat_currencies_full_names[fiat]
    
    # Send a GET request
    url = "https://www.x-rates.com/historical/?from=USD&amount=1&date=" + date
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the historical price data
    table = soup.find('table', {'class': "tablesorter ratesTable"})

    # Convert to pandas dataframe
    df_table = pd.read_html(StringIO(str(table)))[0]
    
    # Clean the data
    df_table_currency = df_table['US Dollar']
    df_table = df_table[(df_table_currency == fiat_currency)]
    fiat_to_USD_conversion_rate = df_table["inv. 1.00 USD"].iloc[0]
    
    return fiat_to_USD_conversion_rate

def get_USD_to_fiat_conversion_rate(date, fiat):
    
    # Get fiat currency
    fiat_currency = fiat_currencies_full_names[fiat]
    
    # Send a GET request
    url = "https://www.x-rates.com/historical/?from=USD&amount=1&date=" + date
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the historical price data
    table = soup.find('table', {'class': "tablesorter ratesTable"})

    # Convert to pandas dataframe
    df_table = pd.read_html(StringIO(str(table)))[0]
    
    # Clean the data
    df_table_currency = df_table['US Dollar']
    df_table = df_table[(df_table_currency == fiat_currency)]
    USD_to_fiat_conversion_rate = df_table["1.00 USD"].iloc[0]
    
    return USD_to_fiat_conversion_rate


def get_price(date, ticker, fiat):

    # Error handling
    if not isValidCurrency(ticker): return None     # TODO: Add actual error handling
    if not isValidCurrency(fiat): return None       # TODO: Add actual error handling

    # Get average USD price of currency
    if isUSDollar(ticker):
        average_USD_price = 1
    elif isFiat(ticker):
        average_USD_price = get_fiat_to_USD_conversion_rate(date, ticker)
    else:
        if is_average_USD_price_crypto_stored_locally(date, ticker):
            average_USD_price = get_average_USD_price_crypto_locally(date, ticker)
        else:
            average_USD_price = get_average_USD_price_crypto_API(date, ticker)

    # Get fiat to USD conversion rate at date
    if isUSDollar(fiat):
        fiat_price = average_USD_price
        # print(ticker + ":")
        # print(f'Average USD price: {str(average_USD_price)}')
        # print(f'Fiat price: {str(fiat_price)}')
        return fiat_price
    
    USD_to_fiat_conversion_rate = get_USD_to_fiat_conversion_rate(date, fiat)

    # Get fiat_price of currency on input date
    fiat_price = average_USD_price * USD_to_fiat_conversion_rate
    # print(f'{fiat}: {str(fiat_price)}')

    # print(ticker + ":")
    # print(f'Average USD price: {str(average_USD_price)}')
    # print(f'USD to {fiat} conversion rate: {str(USD_to_fiat_conversion_rate)}')
    # print(f'Fiat price: {str(fiat_price)}')

    return fiat_price


### Helper Methods ###

def get_formatted_date(date):
    
    day = date[8:]
    month = date[5:7]
    year = date[:4]
    
    formatted_date = day + "-" + month + "-" + year   
    return formatted_date

def get_start_date_string(date):
    
    # Example:
    # - date = 2022-11-15
    # - start_date_string = 20221115
    
    date_string = date.replace("-", "")
    
    return date_string

def get_end_date_string(date_string):
    
    # Example:
    # - date_string = 20221115
    # - end_date_string = 20221116

    year = date_string[:4]
    month = date_string[4:6]
    day = date_string[6:]

    if isNewYear(month, day):
        next_year = str(int(year) + 1)
        next_month = '01'
        next_day = '01'
        end_date_string = next_year + next_month + next_day
    elif isNewMonth(month, day):
        if int(month) < 9:
            next_month = '0' + str(int(month) + 1)
        else:
            next_month = str(int(month) + 1)
        next_day = '01'
        end_date_string = year + next_month + next_day
    else:
        if int(day) < 9:
            next_day = '0' + str(int(day) + 1)
        else:
            next_day = str(int(day) + 1)
        end_date_string = year + month + next_day
        
    return end_date_string

def isNewYear(month, day):
    
    if isNewMonth(month, day):
        if month == '12':
            print('New Year')
            return True
        
    return False

def isNewMonth(month, day):
    
    if day == days_in_months[month]:
        return True
    
    return False

def get_supported_coins() -> dict:
    
    # Format: {ticker: name}
    with open('coin_data/supported_coins.json') as json_file:
        coins_dictionary = json.load(json_file)
    
    return coins_dictionary

def is_average_USD_price_crypto_stored_locally(date, ticker) -> bool:
    
    with open(f'coin_data/coins_market_data.json', "r") as f:
        data = json.load(f)
        if ticker in data and date in data[ticker]:
            return True
        else:
            return False
    
    
# NOTE: Not used
def get_timestamp_format(date):
    timestamp = time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())
    return timestamp

# NOTE: Single time usage
def store_supported_coins():
    
    # Send a GET request
    # - Use /coins/list endpoint
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    
    coins_json = json.loads(response.text)
    with open('coin_data/supported_coins_raw.json', 'w') as outfile:
        outfile.write(json.dumps(coins_json, indent=4))
    
    return None

def reorganize_supported_coins():
    
    with open('coin_data/supported_coins_raw.json') as json_file:
        coins_json = json.load(json_file)
    
    supported_coins = dict()
    for coin in coins_json:
        supported_coins[coin["name"]] = coin["id"]
    
    with open('coin_data/supported_coins.json', 'w') as outfile:
        outfile.write(json.dumps(supported_coins, indent=4))
    
    return None


date = "2023-01-01"
date_string = "20230228"

# get_average_price_crypto(date, "LTC")
# get_fiat_to_USD_conversion_rate(date, "NOK")
# get_USD_to_fiat_conversion_rate(date, 'NOK')
# print(get_price(date, "BTC", "NOK"))

# store_supported_coins()
# reorganize_supported_coins()
# supported_coins = get_supported_coins()
# print(supported_coins["Bitcoin"])
# print(supported_coins["BITCOIN"])