# Functions
# - get_transactions_from_file
# - get_transactions_from_files

from rest.calculations.readers import get_reader, read_file

def get_transactions_from_file(exchange, file_path):

    # Get reader
    reader = get_reader(exchange)

    # Read file
    transactions = read_file(reader, file_path)

    return transactions

def get_transactions_from_files(files):

    # Define files
    index_exchange = 0
    index_file_path = 1

    # Initialize transactions
    transactions = []

    # Get and add file transactions to transactions 
    for file in files:
        exchange = file[index_exchange]
        file_path = file[index_file_path]
        file_transactions = get_transactions_from_file(exchange, file_path)
        transactions += file_transactions                      # TODO: Check that transactions are merged

    return transactions