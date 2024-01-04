#Filer:
# / Overview
# / Fileretriever (Add upload feature, fix TODOs)
# / Readers
# X Datacleaner
# X Datastructures
# / Priceretriever
# X Calculation (Add features, fix TODOs)
# X Writer (Add features, fix TODOs)
# / Visualization

from readers import get_files
from datacleaner import get_transactions_from_files
from calculation import calculate_profit
from writer import write_to_excel


def run():

    order = "FIFO"                      # TODO: User input
    fiat = "USD"                        # TODO: User input

    # TODO: Move validation of order and fiat from calculate_profit to run()?

    files = get_files()
    print('Finished getting files.')
    transactions = get_transactions_from_files(files)
    print('Finished getting transactions.')
    amounts, transaction_profits, currency_transaction_profits, currency_profits, amounts_history = calculate_profit(transactions, order, fiat)
    print()
    print('Finished calculating profits.')
    print()
    write_to_excel(transactions, amounts, transaction_profits, currency_transaction_profits, currency_profits, amounts_history=amounts_history)
    print()
    print('Finished writing to excel.')

    ##visualize(transactions, amounts, transaction_profits, currency_profits)
    
run()


# Things to do:
# - / Get files
# - Specify readers
# - / Get prices (scraping or API)
# - X Write to file (to excel)
# - Visualize on website