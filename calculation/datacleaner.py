# Functions
# - get_transactions_from_file
# - get_transactions_from_files

from readers import get_reader
from readers import read_file

def get_transactions_from_file(exchange, filedata):

    # Get reader
    reader = get_reader(exchange)

    # Read file
    transactions = read_file(reader, filedata)

    return transactions

def get_transactions_from_files(files):

    # Define files
    index_exchange = 0
    index_file_data = 1

    # Initialize transactions
    transactions = []

    # Get and add file transactions to transactions 
    for file in files:
        exchange = file[index_exchange]
        file_data = file[index_file_data]
        file_transactions = get_transactions_from_file(exchange, file_data)
        transactions.append(file_transactions)                      # TODO: Check that transactions are merged

    return transactions