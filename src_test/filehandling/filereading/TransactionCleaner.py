from readers import ExchangeReaders

class TransactionCleaner:
    
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
            transactions.append(file_transactions)                      # TODO: Check that transactions are merged

        return transactions
    
    def get_transactions_from_file(self, exchange, file_path):

        # Get reader
        reader = ExchangeReaders().get_reader(exchange)

        print(file_path)

        # Read file
        transactions = ExchangeReaders().read_file(reader, file_path)

        return transactions