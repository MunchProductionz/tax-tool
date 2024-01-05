import requests
import json
import os
import bs4 as BeautifulSoup
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
from utils import VariablesHolder

class PriceRetriever:
    
    def __init__(self):
        self.utils = VariablesHolder()
    
    def get_price(self, date, ticker, fiat) -> float:

        # Error handling
        if not self.utils.isValidCurrency(ticker): return None     # TODO: Add actual error handling
        if not self.utils.isValidCurrency(fiat): return None       # TODO: Add actual error handling

        # Get average USD price of currency
        if self.utils.isUSDollar(ticker):
            average_USD_price = 1
        elif self.utils.isFiat(ticker):
            average_USD_price = self.get_fiat_to_USD_conversion_rate(date, ticker)
        else:
            if self.is_average_USD_price_crypto_stored_locally(date, ticker):
                average_USD_price = self.get_average_USD_price_crypto_locally(date, ticker)
            else:
                average_USD_price, market_data_USD = self.get_average_USD_price_crypto_API(date, ticker)
                self.add_coin_market_data_USD(ticker, date, market_data_USD)

        # Get fiat to USD conversion rate at date
        if self.utils.isUSDollar(fiat):
            fiat_price = average_USD_price
            return fiat_price
        
        USD_to_fiat_conversion_rate = self.get_USD_to_fiat_conversion_rate(date, fiat)

        # Get fiat_price of currency on input date
        fiat_price = average_USD_price * USD_to_fiat_conversion_rate

        return fiat_price
    
    
    ### Retrieval Methods ###
    
    def get_average_USD_price_crypto_API(self, date, ticker) -> tuple(float, dict):
    
        # Get CoinGecko API key
        load_dotenv()
        api_key = os.environ["COINGECKO_API_KEY"]
        
        # Get the id of the currency
        supported_coins = self.get_supported_coins()
        currency = self.utils.cryptocurrencies_full_names[ticker]
        currency_id = supported_coins[currency]
        
        # Format date
        formatted_date = date.strftime("%d-%m-%Y")
        
        # Send a GET request: /coins/{id}/history endpoint
        url = "https://api.coingecko.com/api/v3/coins/" + currency_id + "/history?date=" + formatted_date + "&x_cg_demo_api_key=" + api_key
        response = requests.get(url)
        response_json = json.loads(response.text)
        
        average_price = response_json["market_data"]["current_price"]["usd"]
        market_data_USD = {
                "current_price": response_json["market_data"]["current_price"]["usd"],
                "market_cap": response_json["market_data"]["market_cap"]["usd"],
                "total_volume": response_json["market_data"]["total_volume"]["usd"],
            }
        
        return average_price, market_data_USD

    def get_average_USD_price_crypto_locally(self, date, ticker) -> float:

        with open(f'coin_data/coins_market_data.json', "r") as f:
            data = json.load(f)
            formatted_date = date.strftime("%Y-%m-%d")
            average_price = data[ticker][formatted_date]["current_price"]
        
        return average_price

    def get_fiat_to_USD_conversion_rate(self, date, fiat) -> float:
        
        # Get fiat currency
        fiat_currency = self.utils.fiat_currencies_full_names[fiat]
        
        # Format date
        formatted_date = date.strftime("%Y-%m-%d")
        
        # Send a GET request
        url = "https://www.x-rates.com/historical/?from=USD&amount=1&date=" + formatted_date
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

    def get_USD_to_fiat_conversion_rate(self, date, fiat) -> float:
        
        # Get fiat currency
        fiat_currency = self.utils.fiat_currencies_full_names[fiat]
        
        # Format date
        formatted_date = date.strftime("%Y-%m-%d")
        
        # Send a GET request
        url = "https://www.x-rates.com/historical/?from=USD&amount=1&date=" + formatted_date
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
    

    ### Helper Methods ###

    def get_supported_coins(self) -> dict:
    
        # Format: {ticker: name}
        with open('coin_data/supported_coins.json') as json_file:
            coins_dictionary = json.load(json_file)
        
        return coins_dictionary

    def is_average_USD_price_crypto_stored_locally(self, date, ticker) -> bool:
    
        with open(f'coin_data/coins_market_data.json', "r") as f:
            data = json.load(f)
            if ticker in data and date.strftime("%Y-%m-%d") in data[ticker]:
                return True
            else:
                return False

    def add_coin_market_data_USD(self, ticker, date, market_data_USD) -> None:
    
        # Handle when market data does not exist
        if market_data_USD == None:
            return None
        
        date_string = date.strftime("%Y-%m-%d")
        
        # Currency does/does not exist, date does not exist
        try:
            with open(f'coin_data/coins_market_data.json', "r") as f:
                data = json.load(f)
                if ticker not in data:
                    data[ticker] = {}
                data[ticker][date_string] = market_data_USD
                new_data = json.dumps(data, indent=4)
            with open(f'coin_data/coins_market_data.json', "w") as f:
                f.write(new_data)
        # File does not exist
        except FileNotFoundError:
            with open(f'coin_data/coins_market_data.json', "w") as f:
                data = {}
                data[ticker] = {}
                data[ticker][date_string] = market_data_USD
                new_data = json.dumps(data, indent=4)
                f.write(new_data)