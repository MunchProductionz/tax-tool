from BinanceReader import BinanceReader
from CoinbaseReader import CoinbaseReader

# Contains all exchange readers
class ExchangeReaders:
    
    def __init__(self):
        # self.readers = self.get_readers()         # TODO: Use this?
        self.reader = {                             # TODO: Or use this?
            "Binance": BinanceReader(),
            "Coinbase": CoinbaseReader()
        }
    
     # Get reader
    def get_reader(self, exchange):

        # Get readers
        readers = self.readers

        # Validations
        if not self.isValidExchange(exchange): return None                       # TODO: Fix error handling

        return readers[exchange]

    def read_file(self, reader, file_path):

        # Use reader to read filedata
        transactions = reader.read_file(file_path)

        return transactions

    ## Help methods ##
    def isValidExchange(self, exchange):
        
        readers = self.readers
        
        for reader_exchange in readers:
            if exchange == reader_exchange: return True
        return False
    
    def get_exchanges(self):
        
        exchanges = [
            "Binance",
            "Coinbase"
        ]
        
        return exchanges

    def get_readers(self):
        
        readers = {
            "Binance": BinanceReader(),
            "Coinbase": CoinbaseReader()
        }
        
        return readers