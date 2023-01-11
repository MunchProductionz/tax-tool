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
                price_sold = 1 / price_bought
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
        
        time_format = get_time_format()
        
        # CSV
        uncleaned_data = pd.read_csv(r'' + file_path + '', delimiter=',', quotechar='"', skiprows=7)
        
        # cleaned_data = uncleaned_data[["Date(UTC)"]]
        cleaned_data = uncleaned_data[["Timestamp", "Transaction Type", "Asset", "Quantity Transacted", "USD Spot Price at Transaction", "USD Subtotal"]]
        
        print(cleaned_data.head())
        
        
        transactions = []
        
        for row in range(len(cleaned_data)):
            date = cleaned_data["Date"].loc[row]
            date_formatted = date.strftime(time_format)
            type = cleaned_data["Transaction Type"].loc[row]
            note = cleaned_data["Notes"].loc[row]
            second_currency = get_currency_from_end_of_note(note)
            
            if type == 'SELL':
                currency_sold = cleaned_data["Asset"].loc[row]
                price_sold = cleaned_data["USD Spot Price at Transaction"].loc[row]
                amount_sold = cleaned_data["Quantity Transacted"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = get_amount_from_end_of_note(note)
            elif type == 'BUY':
                currency_bought = cleaned_data["Asset"].loc[row]
                price_bought = cleaned_data["USD Spot Price at Transaction"].loc[row]
                amount_bought = cleaned_data["Quantity Transacted"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = get_amount_from_end_of_note(note)
            else:
                break
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)


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

def get_currency_from_end_of_note(note):
    
    currencies = get_currencies()
    currency = None
    
    for ticker in range(len(note)-1, 1, -1):
        if note[ticker:] in currencies:
            currency = note[ticker:]
    
    return currency    # TODO: Handle when ticker is invalid

def get_amount_from_end_of_note(note):
    
    currency = get_currency_from_end_of_note(note)
    amount = 0
    
    for number in range(len(note)-len(currency)-1, 1, -1):
        if note[number:number + 1] == " ":
            amount = int(note[number:len(note)-len(currency)-1])
            
    return amount

def get_time_format():
    
    return '%Y-%m-%d %X'


### Testing ###

files = get_files()
readers = get_readers()
exchange = files[1][0]
file_path = files[1][1]
print(files)
print(file_path)
read_file(readers[exchange], file_path)


# reader = BinanceReader()
# reader.read_file()