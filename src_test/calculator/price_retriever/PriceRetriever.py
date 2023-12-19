import requests
import bs4 as BeautifulSoup
import pandas as pd
from variables import VariablesHolder

class PriceRetriever:
    
    def get_price(self, date, ticker, fiat):

        # Error handling
        if not self.isValidCurrency(ticker): return None     # TODO: Add actual error handling
        if not self.isValidCurrency(fiat): return None       # TODO: Add actual error handling

        # Get average USD price of currency
        if self.isUSDollar(ticker):
            average_USD_price = 1
        elif self.isFiat(ticker):
            average_USD_price = self.get_fiat_to_USD_conversion_rate(date, ticker)
        else:
            average_USD_price = self.get_average_USD_price_crypto(date, ticker)

        # Get fiat to USD conversion rate at date
        if self.isUSDollar(fiat):
            fiat_price = average_USD_price
            return fiat_price
        
        USD_to_fiat_conversion_rate = self.get_USD_to_fiat_conversion_rate(date, fiat)

        # Get fiat_price of currency on input date
        fiat_price = average_USD_price * USD_to_fiat_conversion_rate
        print(f'{fiat}: {str(fiat_price)}')

        return fiat_price
    
    def get_fiat_to_USD_conversion_rate(self, date, fiat):
        
        # Get fiat currency
        fiat_currency = VariablesHolder().get_fiat_currencies_full_names()[fiat]
        
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
        fiat_to_USD_conversion_rate = df_table["inv. 1.00 USD"].iloc[0]
        
        return fiat_to_USD_conversion_rate
    
    def get_average_USD_price_crypto(self, date, ticker):
    
        # Use ticker to get name of currency
        currencies_full_names_lowercase = self.convert_values_to_lowercase(VariablesHolder().get_cryptocurrencies_full_names())
        currency = currencies_full_names_lowercase[ticker]
        
        # Get start and end date
        start_date = self.get_start_date_string(date)
        end_date = self.get_end_date_string(start_date)
        
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
        average_price = self.get_average_price(opening_price_usd, closing_price_usd)
        
        return average_price

    def get_USD_to_fiat_conversion_rate(self, date, fiat):
        
        # Get fiat currency
        fiat_currency = VariablesHolder().get_fiat_currencies_full_names()[fiat]
        
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
    


    ### Helper Methods ###

    def get_start_date_string(self, date):
        
        # Example:
        # - date = 2022-11-15
        # - start_date_string = 20221115
        
        date_string = date.replace("-", "")
        
        return date_string

    def get_end_date_string(self, date_string):
        
        # Example:
        # - date_string = 20221115
        # - end_date_string = 20221116

        year = date_string[:4]
        month = date_string[4:6]
        day = date_string[6:]

        if self.isNewYear(month, day):
            next_year = str(int(year) + 1)
            next_month = '01'
            next_day = '01'
            end_date_string = next_year + next_month + next_day
        elif self.isNewMonth(month, day):
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

    def isNewYear(self, month, day):
        
        if self.isNewMonth(month, day):
            if month == '12':
                print('New Year')
                return True
            
        return False

    def isNewMonth(self, month, day):
        
        if day == VariablesHolder().days_in_months()[month]:
            return True
        
        return False

    def get_average_price(self, opening_price_string, closing_price_string):
        
        opening_price_int = self.get_price_int(opening_price_string)
        closing_price_int = self.get_price_int(closing_price_string)
        
        return (opening_price_int + closing_price_int) / 2

    def get_price_int(self, price_string):
        
        # TODO: Fix to fully account for floats (it currently removes everything after '.')
        price_string_no_dollar_sign = price_string.replace('$', '')
        price_string_no_comma = price_string_no_dollar_sign.replace(',', '')
        if '.' in price_string_no_comma:
            price_string_no_comma = price_string_no_comma[:price_string_no_comma.index('.')]
        price_int = int(price_string_no_comma)
        
        return price_int