import pandas as pd
import glob
import re
import csv
import io
from datetime import datetime

#Functions:
# - *Define readers ({exchange: <reader>})
# - get_files
# - get_reader
# - read_file
# - *initialize_exchange_readers?


### Methods ###

# Get uploaded files
def get_files():

    # TODO: Create method for storing files
    # TODO: Separate between different exchanges
    # TODO: Handle case when file is not valid type

    # Create lists of uploaded files
    files = list()          # TODO: Rewrite to use dictionary with lists instead of 2D-list
    
    # Get valid exchanges
    exchanges = get_exchanges()

    # Add uploaded files' file_path and their exchanges to files
    for exchange in exchanges:
        for file_path in glob.glob("../files/*" + exchange + "*"):
            files.append([exchange, file_path])

    return files

# Get reader
def get_reader(exchange):

    # Get readers
    readers = get_readers()

    # Validations
    if not isValidExchange(exchange): return None                       # TODO: Fix error handling

    return readers[exchange]

def read_file(reader, file_path):

    # Use reader to read filedata
    transactions = reader.read_file(file_path)

    return transactions


### Readers ###

# BinanceReader
class BinanceReader:

    def read_file(self, file_path):
        
        time_format = get_time_format()
        
        # Excel
        # uncleaned_data = pd.read_excel(filedata)      # TODO: Implement if possible to input file
        uncleaned_data = pd.read_excel(r'' + file_path + '')
        
        # Columns:
        # - 'Date'      date
        # - 'Market'    first_currency + second_currency
        # - 'Type'      transaction_type
        # - 'Price'     price_sold + price_bought=1/price_sold
        # - 'Amount'    SELL -> amount_sold, BUY -> amount_bought
        # - 'Total'     SELL -> amount_bought, BUY -> amount_sold
        # - 'Fee'
        # - 'Fee Coin'
        
        cleaned_data = uncleaned_data[["Date", "Market", "Type", "Price", "Amount", "Total"]]
        
        transactions = []
        
        for row in range(len(cleaned_data)):
            date = cleaned_data["Date"].loc[row]
            date_formatted = date.to_pydatetime()               # Change from pandas timestamp to datetime
            transaction_type = cleaned_data["Type"].loc[row]
            market = cleaned_data["Market"].loc[row]
            first_currency = get_first_currency(market)
            second_currency = market[len(first_currency):]
            
            if transaction_type == 'SELL':
                currency_sold = first_currency
                price_sold = cleaned_data["Price"].loc[row]
                amount_sold = cleaned_data["Amount"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = cleaned_data["Total"].loc[row]
            else:
                currency_bought = first_currency
                price_bought = cleaned_data["Price"].loc[row]
                amount_bought = cleaned_data["Total"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = cleaned_data["Amount"].loc[row]
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)
        
        return transactions

# CoinbaseReader
class CoinbaseReader:

    def read_file(self, file_path):
        
        time_format = get_time_format()
        number_of_rows_skipped = 7

        processed_lines = []

        with open(file_path, 'r') as file:
            for _ in range(number_of_rows_skipped):
                next(file)

            for line in file:
                if line.startswith('"') and line.endswith('"\n'):
                    line = line[1:-2] + '\n'    # Removes ""
                line = line.replace('""', '"')
                processed_lines.append(line)

        cleaned_data = ''.join(processed_lines)
        cleaned_string_buffer = io.StringIO(cleaned_data)
        data = pd.read_csv(cleaned_string_buffer)
        
        # Columns:
        # - 'Timestamp'                                 date
        # - 'Transaction Type'                          transaction_type
        # - 'Asset'                                     Sell -> currency_sold, Buy -> currency_bought
        # - 'Quantity Transacted',                      Sell -> amount_sold, Buy -> amount_bought
        # - 'Spot Price Currency'       
        # - 'Spot Price at Transaction'                 Sell -> price_sold, price_bought=1/price_sold, Buy -> price_bought, price_sold=1/price_bought
        # - 'Subtotal'
        # - 'Total (inclusive of fees and/or spread)'
        # - 'Fees and/or Spread'
        # - 'Notes'
        
        transactions = []
        
        for row in range(len(data)):
            date = data["Timestamp"].loc[row]
            date_formatted = datetime.strptime(date, time_format)
            transaction_type = data["Transaction Type"].loc[row]
            note = data["Notes"].loc[row]
            second_currency = get_currency_from_end_of_note(note)
            
            if transaction_type == 'Sell':
                currency_sold = data["Asset"].loc[row]
                price_sold = data["Spot Price at Transaction"].loc[row]
                amount_sold = data["Quantity Transacted"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = get_amount_from_end_of_note(note)
            elif transaction_type == 'Buy':
                currency_bought = data["Asset"].loc[row]
                price_bought = data["Spot Price at Transaction"].loc[row]
                amount_bought = data["Quantity Transacted"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = get_amount_from_end_of_note(note)
            else:
                # Ignore 'Send' and 'Receive'
                continue
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)
        
        return transactions

# ...


### Helper methods ###

def isValidExchange(exchange):
    
    readers = get_readers()
    
    for reader_exchange in readers:
        if exchange == reader_exchange: return True
    return False

def get_exchanges():
    
    exchanges = [
        "Binance",
        "Coinbase"
    ]
    
    return exchanges

def get_readers():
    
    readers = {
        "Binance": BinanceReader(),
        "Coinbase": CoinbaseReader()
    }
    
    return readers

def get_currencies():
    
    currencies = [
        "BTC",
        "ETH",
        "LTC",
        "XRP",
        "POWR",
        "USD"
    ]

    return currencies
    
def get_first_currency(market):
    
    currencies = get_currencies()
    first_currency = None
    
    for ticker in range(1, len(market)-1):
        if market[:ticker] in currencies:
            first_currency = market[:ticker]
    
    return first_currency    # TODO: Handle when ticker is invalid

def get_currency_from_end_of_note(note):
    
    currencies = get_currencies()
    currency = None
    
    for ticker in range(len(note)-1, 1, -1):
        if note[ticker:] in currencies:
            currency = note[ticker:]
    
    return currency    # TODO: Handle when ticker is invalid

def get_amount_from_end_of_note(note):
    
    # Remove the currency and space from the end of the note
    currency = get_currency_from_end_of_note(note)
    end_of_note_minus_space_and_currency = len(note)-len(currency)-1
    new_note = note[:end_of_note_minus_space_and_currency]

    # Find the last space in the new_note
    last_space_index = new_note.rfind(" ")

    # Extract the amount string from the note
    amount_string = new_note[last_space_index + 2:]

    # Replace commas with an empty string to handle thousands separators
    amount_string = amount_string.replace(",", "")

    # Convert the amount string to a float
    amount = float(amount_string)

    return amount

# def get_time_format():
    
#     return '%Y-%m-%d %X'

def get_time_format():
    
    return '%Y-%m-%dT%H:%M:%SZ'


### Testing ###

# files = get_files()
# readers = get_readers()

# exchange = files[0][0]      # Binance file
# file_path = files[0][1]
# exchange = files[1][0]      # Coinbase file
# file_path = files[1][1]
# print(exchange)

# for files in files:
#     exchange = files[0]
#     file_path = files[1]
#     read_file(readers[exchange], file_path)
    
# read_file(readers[exchange], file_path)


# reader = BinanceReader()
# reader.read_file()