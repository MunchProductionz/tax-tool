import pandas as pd
import glob

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
    files = list()
    
    # Get valid exchanges
    exchanges = get_exchanges()

    # Add uploaded files' file_path and their exchanges to files
    for exchange in exchanges:
        for file_path in glob.glob("../files/*" + exchange + "*"):
            files.append([exchange, file_path])

    print(files)

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
        cleaned_data = uncleaned_data[["Date", "Market", "Type", "Price", "Amount", "Total"]]
        
        print(cleaned_data.head())
        
        transactions = []
        
        for row in range(len(cleaned_data)):
            date = cleaned_data["Date"].loc[row]
            date_formatted = date.strftime(time_format)
            type = cleaned_data["Type"].loc[row]
            market = cleaned_data["Market"].loc[row]
            first_currency = get_first_currency(market)
            second_currency = market[len(first_currency):]
            
            if type == 'SELL':
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
                price_sold = 1 / price_sold
                amount_sold = cleaned_data["Amount"].loc[row]
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return transactions

# CoinbaseReader
class CoinbaseReader:

    def read_file(self, file_path):
        
        # CSV
        uncleaned_data = pd.read_csv(r'' + file_path + '')
        print(uncleaned_data.head())
    
        # cleaned_data = uncleaned_data[["Date(UTC)"]]

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None

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

def get_time_format():
    
    return '%Y-%m-%d %X'

### Testing ###

files = get_files()
readers = get_readers()
exchange = files[0][0]
file_path = files[0][1]
print(files)
print(file_path)
read_file(readers[exchange], file_path)


# reader = BinanceReader()
# reader.read_file()