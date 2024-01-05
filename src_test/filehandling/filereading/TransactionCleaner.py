from ExchangeReaders import ExchangeReaders

class TransactionCleaner:
    
    def __init__(self):
        self.exchange_readers = ExchangeReaders()
    
    def get_transactions_from_files(self, files):

        # Define files
        index_exchange = 0
        index_file_path = 1

        # Initialize transactions
        transactions = []

        # Get and add file transactions to transactions 
        for file in files:
            exchange = file[index_exchange]
            file_path = file[index_file_path]
            file_transactions = self.get_transactions_from_file(exchange, file_path)
            if file_transactions is not None:
                transactions += file_transactions
            else:
                print("Error: No transactions found in " + file_path)

        return transactions
    
    def get_transactions_from_file(self, exchange, file_path):

        # Get reader and read file
        reader = self.exchange_readers.get_reader(exchange)
        transactions = self.exchange_readers.read_file(reader, file_path)

        return transactions