#Functions:
# - *Define readers ({exchange: <reader>})
# - get_files
# - find_reader
# - read_file
# - *initialize_exchange_readers?

readers = {}

# Get uploaded files
def get_files():

    # Return list of uploaded files

    return None

# Get reader
def get_reader(exchange):

    # Validations
    if not isValidExchange(exchange):
        return None                                         # TODO: Fix error handling

    return readers[exchange]

def read_file(reader, filedata):

    # Use reader to read filedata
    # Return transactions
    # TODO: Fix

    return None



# Helper methods
def isValidExchange(exchange):
    for reader_exchange, reader in readers:
        if exchange == reader_exchange: return True
    return False