import pandas as pd

#Functions:
# - *Define readers ({exchange: <reader>})
# - get_files
# - get_reader
# - read_file
# - *initialize_exchange_readers?


### Methods ###

# Get uploaded files
def get_files():

    # Return list of uploaded files

    return None

# Initialize readers
def initialize_readers():
    
    # Initialize readers-dictionary

    return None

# Get reader
def get_reader(exchange):

    # Validations
    if not isValidExchange(exchange): return None                       # TODO: Fix error handling

    return readers[exchange]

def read_file(reader, filedata):

    # Use reader to read filedata
    transactions = reader.read_file(filedata)

    return transactions


### Readers ###

# BinanceReader
class BinanceReader:

    def read_file(filedata):
        
        # Excel
        uncleaned_data = pd.read_excel(filedata)
        # data = pd.read_excel(r'Path where the Excel file is stored\File name.xlsx')

        cleaned_data = uncleaned_data[["Date(UTC)"]]
        cleaned_data

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None

# CoinbaseReader
class CoinbaseReader:

    def read_file(filedata):
        
        # CSV

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None

# ...


readers = {
    "Binance": BinanceReader(),
    "Coinbase": CoinbaseReader()
}



### Helper methods ###

def isValidExchange(exchange):
    for reader_exchange, reader in readers:
        if exchange == reader_exchange: return True
    return False