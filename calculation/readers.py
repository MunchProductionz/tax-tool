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

    def read_file(file_path):
        
        # Excel
        # uncleaned_data = pd.read_excel(filedata)      # TODO: Implement if possible to input file
        uncleaned_data = pd.read_excel(r'' + file_path + '')
        print(uncleaned_data.head())
    
        cleaned_data = uncleaned_data[["Date(UTC)"]]

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None

# CoinbaseReader
class CoinbaseReader:

    def read_file(file_path):
        
        # CSV
        uncleaned_data = pd.read_csv(r'' + file_path + '')
        print(uncleaned_data.head())
    
        cleaned_data = uncleaned_data[["Date(UTC)"]]

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None

# ...


### Helper methods ###

def isValidExchange(exchange):
    
    readers = get_readers()
    
    for reader_exchange, reader in readers:
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

### Testing ###

get_files()


# reader = BinanceReader()
# reader.read_file()