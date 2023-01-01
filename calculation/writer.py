import xlsxwriter

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# Transaction_profits: {[currency]: [date, profit], ...}
# Currency_profits: {[currency]: profit, ...}

def write_to_excel(transactions, transaction_profits, currency_profits):

    # Initialization
    workbook, transactions_sheet, assets_sheet = initialize_workbook_and_worksheets()

    # Fix worksheets
    write_transactions_sheet(transactions, transaction_profits, transactions_sheet)
    write_assets_sheet(transactions, currency_profits, assets_sheet)

    # Profit per transaction
    # - Write each transaction to a new line in excel
    # - Write each transaction_profit to a new line in excel
    # TODO: Fix



    # Assets and total profit per currency
    # - Write each transaction to a new line in excel (debit/credit per currency)
    # - Write currency_profit per currency

    return None

def write_transactions_sheet(transactions, transactions_profits, transactions_sheet):
    
    return None

def write_assets_sheet(transactions, currency_profits, assets_sheet):
    
    return None


### Helper Methods ###
def initialize_workbook_and_worksheets():
    workbook = xlsxwriter.Workbook('tax_info.xlsx')
    transactions_sheet = workbook.add_worksheet('Transactions')
    assets_sheet = workbook.add_worksheet('Assets')
    
    return workbook, transactions_sheet, assets_sheet