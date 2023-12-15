from readers import FileReader
from datacleaner import TransactionCleaner
from calculator import ProfitCalculator
from writer import ExcelWriter

# Controller
def run():

    order = "FIFO"                      # TODO: User input
    fiat = "USD"                        # TODO: User input

    # TODO: Move validation of order and fiat from calculate_profit to run()?
    files = FileReader().get_files()                                                                                    # Uses FileReader
    transactions = TransactionCleaner().get_transactions_from_files(files)                                              # Uses TransactionCleaner and ExchangeReaders
    amounts, transaction_profits, currency_profits = ProfitCalculator().calculate_profit(transactions, order, fiat)     # Uses ProfitCalculator, PriceRetriever and VariablesHolder
    ExcelWriter().write_to_excel(transactions, amounts, transaction_profits, currency_profits)                          # Uses ExcelWriter