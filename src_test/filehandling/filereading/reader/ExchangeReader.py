

# Contains all exchange readers
class ExchangeReaders:
    
     # Get reader
    def get_reader(self, exchange):

        # Get readers
        readers = self.get_readers()

        # Validations
        if not self.isValidExchange(exchange): return None                       # TODO: Fix error handling

        return readers[exchange]

    def read_file(self, reader, file_path):

        # Use reader to read filedata
        transactions = reader.read_file(file_path)

        return transactions

    ## Help methods ##
    def isValidExchange(self, exchange):
        
        readers = self.get_readers()
        
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