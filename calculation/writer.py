import xlsxwriter

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# Transaction_profits: {[currency]: [date, profit], ...}
# Currency_profits: {[currency]: profit, ...}

def write_to_excel(transactions, transaction_profits, currency_profits):

    # Initialization
    workbook, transactions_sheet, assets_sheet = initialize_workbook_and_worksheets()
    
    # Formatting
    bold = workbook.add_format({'bold': 1})

    # Fix worksheets
    write_transactions_sheet(transactions, transaction_profits, transactions_sheet, bold)
    write_assets_sheet(transactions, currency_profits, assets_sheet)

    # Profit per transaction
    # - Write each transaction to a new line in excel
    # - Write each transaction_profit to a new line in excel
    # TODO: Fix



    # Assets and total profit per currency
    # - Write each transaction to a new line in excel (debit/credit per currency)
    # - Write currency_profit per currency

    workbook.close()

    return None

def write_transactions_sheet(transactions, transactions_profits, sheet, bold):
    
    # Write headers
    sheet.write('B4', "Date", bold)
    sheet.write('C4', "Currency Sold", bold)
    sheet.write('D4', "Amound Sold", bold)
    sheet.write('E4', "Price Sold", bold)
    sheet.write('F4', "Currency Bought", bold)
    sheet.write('G4', "Amount Bought", bold)
    sheet.write('H4', "Price Bought", bold)
    
    # Write transactions
    transaction_number = 0
    while transaction_number < len(transactions):
        transaction_row = transaction_number + 5        # Starts at row 5
        sheet.write('B' + str(transaction_row), transactions[transaction_number][transaction_index["date"]])
        sheet.write('C' + str(transaction_row), transactions[transaction_number][transaction_index["currency_sold"]])
        sheet.write('D' + str(transaction_row), transactions[transaction_number][transaction_index["amount_sold"]])
        sheet.write('E' + str(transaction_row), transactions[transaction_number][transaction_index["price_sold"]])
        sheet.write('F' + str(transaction_row), transactions[transaction_number][transaction_index["currency_bought"]])
        sheet.write('G' + str(transaction_row), transactions[transaction_number][transaction_index["amount_bought"]])
        sheet.write('H' + str(transaction_row), transactions[transaction_number][transaction_index["price_bought"]])
    
    return None

def write_assets_sheet(transactions, currency_profits, sheet):
    
    return None

# Define transaction
transaction_index = {
    "date": 0,
    "currency_sold": 1,
    "amount_sold": 2,
    "price_sold": 3,
    "currency_bought": 4,
    "amount_bought": 5,
    "price_bought": 6
}


### Helper Methods ###
def initialize_workbook_and_worksheets():
    workbook = xlsxwriter.Workbook('tax_info.xlsx')
    transactions_sheet = workbook.add_worksheet('Transactions')
    assets_sheet = workbook.add_worksheet('Assets')
    
    return workbook, transactions_sheet, assets_sheet



### Testing ###

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = ["01/01/2023", "BTC", 0.5, 25000, "USD", 12500, 1]
cleaned_transaction_2 = ["02/01/2023", "USD", 5000, 1, "USD", 0.25, 20000]
cleaned_transactions = [cleaned_transaction_1, cleaned_transaction_2]

transaction_profits = {"BTC": ["01/01/2023", 10000]}
currency_profits = {"BTC": 10000}






