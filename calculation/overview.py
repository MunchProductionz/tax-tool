#Filer:
# / Overview
# Readers
# Datacleaner
# X Datastructures
# / Priceretriever
# X Calculation (Add features, fix TODOs)
# Writer

from readers import get_files
from datacleaner import get_transactions_from_files
from calculation import calculate_profit
from writer import write_to_excel


def run():

    order = "FIFO"                      # TODO: User input
    fiat = "USD"                        # TODO: User input

    # TODO: Move validation of order and fiat from calculate_profit to run()?

    files = get_files()
    transactions = get_transactions_from_files(files)
    amounts, transaction_profits, currency_profits = calculate_profit(transactions, order, fiat)
    write_to_excel(transactions, transaction_profits, currency_profits)

