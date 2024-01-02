import os
import requests
import json
import time
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
from variables import cryptocurrencies_full_names
from priceretriever import get_supported_coins, get_formatted_date


def get_dates_list(start_date, end_date, requests_per_minute=20):

    # Create range of dates
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = pd.date_range(start_datetime, end_datetime - timedelta(days=1), freq='d')
    dates_list = date_range.strftime('%Y-%m-%d').tolist()           # Ascending order
    # dates_list = date_range.strftime('%Y-%m-%d').tolist().reverse() # Descending order

    # Split dates_list into lists of length requests_per_minute
    dates_list_split = []
    for index in range(0, len(dates_list), requests_per_minute):
        dates_list_split.append(dates_list[index:index + requests_per_minute])
    
    return dates_list_split

def get_market_data_USD_from_API(date, ticker, missing_market_data):
    
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
    
    # Handle when market data does not exist
    if not "market_data" in response_json:
        if not ticker in missing_market_data:
            missing_market_data[ticker] = []
        missing_market_data[ticker].append(date)
        return None
    else:
        market_data_USD = {
            "current_price": response_json["market_data"]["current_price"]["usd"],
            "market_cap": response_json["market_data"]["market_cap"]["usd"],
            "total_volume": response_json["market_data"]["total_volume"]["usd"],
        }
        return market_data_USD

def add_coin_market_data_USD(ticker, date, market_data_USD) -> None:
    
    # Data template
    # currency = {
    #     date: market_data
    # }
    
    # market_data = {
    #     "currenct_price": float,
    #     "market_cap": float,
    #     "total_volume": float,
    # }
    
    # Handle when market data does not exist
    if market_data_USD == None:
        return None
    
    # Currency does/does not exist, date does not exist
    try:
        with open(f'coin_data/coins_market_data.json', "r") as f:
            data = json.load(f)
            if ticker not in data:
                data[ticker] = {}
            data[ticker][date] = market_data_USD
            new_data = json.dumps(data, indent=4)
        with open(f'coin_data/coins_market_data.json', "w") as f:
            f.write(new_data)
    # File does not exist
    except FileNotFoundError:
        with open(f'coin_data/coins_market_data.json', "w") as f:
            data = {}
            data[ticker] = {}
            data[ticker][date] = market_data_USD
            new_data = json.dumps(data, indent=4)
            f.write(new_data)
    
def is_date_stored(ticker, date) -> bool:
    try:
        with open(f'coin_data/coins_market_data.json', "r") as f:
            data = json.load(f)
            if ticker in data and date in data[ticker]:
                return True
            else:
                return False
    except FileNotFoundError:
        return False
    
def sleep_to_avoid_API_rate_limit(call, call_counter_factor, sleep_time):
    if call != 0 and call % call_counter_factor == 0:
        # Wait 3 minutes to reset API url
        time.sleep(sleep_time * 5)
    else:
        # Wait 1 minute
        time.sleep(sleep_time)

    
def add_missing_market_data(missing_market_data):
    number_of_missing_market_data_points = 0
    try:
        with open(f'coin_data/missing_market_data.json', "r") as f:
            data = json.load(f)
            for ticker in missing_market_data:
                number_of_missing_market_data_points += len(missing_market_data[ticker])
                if ticker not in data:
                    data[ticker] = []
                for date in missing_market_data[ticker]:
                    data[ticker].append(date)
            new_data = json.dumps(data, indent=4)
        with open(f'coin_data/missing_market_data.json', "w") as f:
            f.write(new_data)
    except FileNotFoundError:
        with open(f'coin_data/missing_market_data.json', "w") as f:
            data = {}
            for ticker in missing_market_data:
                number_of_missing_market_data_points += len(missing_market_data[ticker])
                data[ticker] = []
                for date in missing_market_data[ticker]:
                    data[ticker].append(date)
            new_data = json.dumps(data, indent=4)
            f.write(new_data)
            
    return number_of_missing_market_data_points


def get_and_store_coin_market_data_USD_from_API(ticker, start_date, end_date, requests_per_minute=20, sleep_time=60) -> float:
    
    # Start timer
    start = time.time()
    
    dates_list = get_dates_list(start_date, end_date, requests_per_minute=requests_per_minute)
    missing_market_data = {}
    call_counter_factor = 26
    
    for call, dates in enumerate(dates_list):
        print(f'Call {call + 1} of {len(dates_list)} started. ({round((100*(call+1)/len(dates_list)))}%)')
        for date in dates:
            if is_date_stored(ticker, date):
                print(f'Date {date} already stored.')
            else:
                market_data_USD = get_market_data_USD_from_API(date, ticker, missing_market_data)
                add_coin_market_data_USD(ticker, date, market_data_USD)
        
        # Sleep 1 min, 3 min every 28 calls
        sleep_to_avoid_API_rate_limit(call, call_counter_factor, sleep_time)
        
        print(f'Call {call + 1} of {len(dates_list)} ended. Last date stored: {dates[-1]}')
        print()

    print()
    print(f'All dates stored. Last date stored: {dates_list[-1][-1]}')

    print()
    number_of_missing_market_data_points = add_missing_market_data(missing_market_data)
    print(f'Missing data added. Number of missing market data points: {number_of_missing_market_data_points}')
    
    # Stop timer
    end = time.time()
    print()
    print(f'Time elapsed: {round(end - start, 2)} seconds')
    
## Testing

start_date = '2023-06-15'
end_date = '2023-12-30'
ticker = 'XRP'
requests_per_minute = 20
sleep_time = 42.8           # Empirically determined, gives ~7 seconds expected std (Average time is 84.21 seconds with 60 sec sleep time, max std is ~6.76 seconds)

# dates_list = get_dates_list(start_date, end_date, requests_per_minute)
# print(dates_list)
# number_of_dates = 0
# for call, dates in enumerate(dates_list):
#     number_of_dates += len(dates)
#     print(f'Call {call + 1}, number of dates: {len(dates)}')
# print(f'Total number of dates: {number_of_dates}')

get_and_store_coin_market_data_USD_from_API(ticker, start_date, end_date, requests_per_minute=requests_per_minute, sleep_time=sleep_time)