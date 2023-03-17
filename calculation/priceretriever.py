import requests
from bs4 import BeautifulSoup
import pandas as pd
from variables import currencies_full_names
from variables import convert_values_to_lowercase
from variables import days_in_months
from variables import isValidCurrency

def get_average_price_crypto(date, ticker):
    
    # Use ticker to get name of currency
    currencies_full_names_lowercase = convert_values_to_lowercase(currencies_full_names)
    currency = currencies_full_names_lowercase[ticker]
    
    # Get start and end date
    start_date = get_start_date_string(date)
    end_date = get_end_date_string(start_date)
    
    # Send a GET request
    url = "https://www.coingecko.com/en/coins/" + currency + "/historical_data/?start_date=" + start_date + "&end_date=" + end_date + "#panel"
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the historical price data
    table = soup.find('table', {'class': "table table-striped text-sm text-lg-normal"})

    # Convert to pandas dataframe
    df_table = pd.read_html(str(table))
    
    # Clean the data
    opening_price_usd = df_table[0]["Open"][1]
    closing_price_usd = df_table[0]["Close"][1]
    
    # Calculate average daily price
    average_price = get_average_price(opening_price_usd, closing_price_usd)
    
    return average_price

def get_USD_to_fiat_conversion_rate(date, fiat):
    
    # Get fiat currency
    fiat_currency = currencies_full_names[fiat]
    
    # Send a GET request
    url = "https://www.x-rates.com/historical/?from=USD&amount=1&date=" + date
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the historical price data
    table = soup.find('table', {'class': "tablesorter ratesTable"})

    # Convert to pandas dataframe
    df_table = pd.read_html(str(table))[0]
    
    # Clean the data
    df_table_currency = df_table['US Dollar']
    df_table = df_table[(df_table_currency == fiat_currency)]
    USD_to_fiat_conversion_rate = df_table["1.00 USD"].iloc[0]
    
    return USD_to_fiat_conversion_rate


def get_price(date, ticker, fiat):

    # TODO: Add actual error handling
    # Error handling
    if not isValidCurrency(ticker): return None
    if not isValidCurrency(fiat): return None

    # Get average USD price of currency
    average_usd_price_crypto = get_average_price_crypto(date, ticker)

    # Get fiat to USD conversion rate at date
    USD_to_fiat_conversion_rate = get_USD_to_fiat_conversion_rate(date, fiat)

    # Get fiat_price of currency on input date
    fiat_price = average_usd_price_crypto * USD_to_fiat_conversion_rate
    print(f'{fiat}: {str(fiat_price)}')

    return fiat_price


### Helper Methods ###

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

def get_average_price(opening_price_string, closing_price_string):
    
    opening_price_int = get_price_int(opening_price_string)
    closing_price_int = get_price_int(closing_price_string)
    
    return (opening_price_int + closing_price_int) / 2

def get_price_int(price_string):
    
    # TODO: Fix to fully account for floats (it currently removes everything after '.')
    price_string_no_dollar_sign = price_string.replace('$', '')
    price_string_no_comma = price_string_no_dollar_sign.replace(',', '')
    if '.' in price_string_no_comma:
        price_string_no_comma = price_string_no_comma[:price_string_no_comma.index('.')]
    price_int = int(price_string_no_comma)
    
    return price_int


date = "2023-02-15"
date_string = "20230228"

# get_average_price_crypto(date, "LTC")
# get_USD_to_fiat_conversion_rate(date, 'NOK')
get_price(date, "BTC", "NOK")