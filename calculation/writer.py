import xlsxwriter
from datetime import date
from datastructures import Stack
from datastructures import Queue
from priceretriever import get_price      # TODO: Add when get_price() is fixed

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# Transaction_profits: {[currency]: [date, profit], ...}
# Currency_profits: {[currency]: profit, ...}

def write_to_excel(transactions, amounts, transaction_profits, currency_transaction_profits, currency_profits, amounts_history=None):

    # Initialization
    workbook, transactions_sheet, results_sheet, assets_sheet = initialize_workbook_and_worksheets()
    
    # Formatting
    format = get_format(workbook)
    
    # Create charts
    bar_chart = get_bar_chart(workbook)
    pie_chart = get_pie_chart(workbook)

    # Fix worksheets
    write_transactions_sheet(transactions_sheet, transactions, transaction_profits, format)
    write_results_sheet(results_sheet, currency_profits, format, bar_chart)
    write_assets_sheet(assets_sheet, transactions, amounts, currency_profits, format, pie_chart)

    # Assets and total profit per currency
    # - Write each transaction to a new line in excel (debit/credit per currency)
    # - Write currency_profit per currency  # TODO: Fix

    workbook.close()

    return None

def write_transactions_sheet(sheet, transactions, transactions_profits, format):
    
    # Get indexes
    transaction_index = get_transaction_index()
    
    # Write headers
    sheet.write('B2', "Transactions", format["sheet_header"])
    sheet.write('B4', "Date", format["column_header"])
    sheet.write('C4', "Currency Sold", format["column_header"])
    sheet.write('D4', "Amount Sold", format["column_header"])
    sheet.write('E4', "Price Sold", format["column_header"])
    sheet.write('F4', "Currency Bought", format["column_header"])
    sheet.write('G4', "Amount Bought", format["column_header"])
    sheet.write('H4', "Price Bought", format["column_header"])
    sheet.write('I4', "Profit", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 15, format["center_align"])
    sheet.set_column(3, 3, 12)
    sheet.set_column(4, 4, 12)
    sheet.set_column(5, 5, 17, format["center_align"])
    sheet.set_column(6, 6, 15)
    sheet.set_column(7, 7, 12)
    sheet.set_column(8, 8, 10, format["center_align"])
    
    # Set conditional format when profit > 0
    sheet.conditional_format('I5:I200', {
                                            'type': 'cell',
                                            'criteria': '>',
                                            'value': 0,
                                            'format': format["green"]})
    
    # Set conditional format when profit < 0
    sheet.conditional_format('I5:I200', {
                                            'type': 'cell',
                                            'criteria': '<',
                                            'value': 0,
                                            'format': format["red"]})
    
    # Write transactions
    row = 5                                # Starts at row 5 (+1)
    for transaction in transactions:
        sheet.write('B' + str(row), transaction[transaction_index["date"]].strftime("%Y-%m-%d"))
        sheet.write('C' + str(row), transaction[transaction_index["currency_sold"]])
        sheet.write('D' + str(row), transaction[transaction_index["amount_sold"]])
        sheet.write('E' + str(row), transaction[transaction_index["price_sold"]])
        sheet.write('F' + str(row), transaction[transaction_index["currency_bought"]])
        sheet.write('G' + str(row), transaction[transaction_index["amount_bought"]])
        sheet.write('H' + str(row), transaction[transaction_index["price_bought"]])
        sheet.write('I' + str(row), transactions_profits[row - 5])                       # List starts at index 0
        row += 1
    
    print('Transaction sheet completed.')    
    
    return None

def write_results_sheet(sheet, currency_profits, format, bar_chart):
    
    # Write headers
    sheet.write('B2', "Results", format["sheet_header"])
    sheet.write('B4', "Currency", format["column_header"])
    sheet.write('C4', "Profit", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 15, format["center_align"])
    
    # Set conditional format when profit > 0
    sheet.conditional_format('C5:C200', {
                                            'type': 'cell',
                                            'criteria': '>',
                                            'value': 0,
                                            'format': format["green"]})
    
    # Set conditional format when profit < 0
    sheet.conditional_format('C5:C200', {
                                            'type': 'cell',
                                            'criteria': '<',
                                            'value': 0,
                                            'format': format["red"]})
    
    # Write profit of currencies
    row = 5         # Starts at row 6 (5+1)
    for currency, profit in currency_profits.items():
        sheet.write('B' + str(row), currency)
        sheet.write('C' + str(row), profit)
        row += 1
    
    # Add series to the bar chart
    bar_chart.add_series({
        'name': '=Results!$B$2',
        'categories': '=Results!$B$5:$B$' + str(row),
        'values': '=Results!$C$5:$C$' + str(row),
        'data_labels': {'value': True, 'num_format': '#,##0.00'}
    })
    
    # Insert chart into sheet
    sheet.insert_chart('D4', bar_chart)
    
    print('Results sheet completed.')   
    
    return None

def write_assets_sheet(sheet, transactions, amounts, currency_profits, format, pie_chart):
    
    # TODO: Allow for initial asset inputs?
    
    # Get indexes
    amount_index = get_amount_index()
    column_index = get_column_index()
    transaction_index = get_transaction_index()
    
    # Get number of transactions
    number_of_transactions = len(transactions)
    
    # Write headers
    sheet.write('B2', "Assets", format["sheet_header"])
    sheet.write('B4', "Currency", format["column_header"])
    sheet.write('C4', "Amount", format["column_header"])
    sheet.write('D4', "Value (USD)", format["column_header"])
    sheet.write('E4', "Value (%)", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 10)
    sheet.set_column(2, 2, 12, format["center_align"])
    sheet.set_column(3, 3, 14, format["center_align"])
    sheet.set_column(4, 4, 10, format["center_align_percentage"])
    
    # Write amount of currencies
    row = 5         # Starts at row 6 (5+1)
    date_today = date.today()
    value_of_currencies = {}                                                                   
    for currency, amount in amounts.items():            # Remember that amount is a datastructure, which cannot be copied (pop permanently removes items from datastructure)
        sheet.write('B' + str(row), currency)
        currency_amount = 0
        while not amount.isEmpty():
            currency_amount += amount.dequeue()[amount_index["amount"]]
        currency_value = get_price(date_today, currency, "USD") * currency_amount      
        value_of_currencies[currency] = currency_value                              
        sheet.write('C' + str(row), currency_amount)
        sheet.write('D' + str(row), currency_value)                                   
        row += 1
        
    # Write % value of currencies                                                          
    row = 5         # Starts at row 6 (5+1)
    sum_value_of_currencies = sum(value_of_currencies.values())                                   
    for currency, currency_value in value_of_currencies.items():
        percentage_of_total_value = currency_value / sum_value_of_currencies
        sheet.write('E' + str(row), round(percentage_of_total_value, 2))
        row += 1
    
    # Add series to the pie chart
    pie_chart.add_series({
        'name': '=Assets!$B$2',
        'categories': '=Assets!$B$5:$B$' + str(row),
        'values': '=Assets!$D$5:$D$' + str(row),          
        'data_labels': {'value': True, 'num_format': '#,##0.00'}
    })
    
    # Insert chart into sheet
    sheet.insert_chart('F4', pie_chart)
    
    
    # Write headers
    sheet.write('N2', "Transactions", format["sheet_subheader"])
    sheet.merge_range('N4:N5', "Date", format["merged_header_left_align_bottom_border"])
    sheet.write('N6', "SUM Total", format["column_header"])
    sheet.write('N7', "SUM", format["column_header"])
    
    # Set column-width, column N
    sheet.set_column(13, 13, 12)
    
    # Write headers for currencies
    row = 3         # Starts at row 4 (zero-indexed)
    column = 14     # Starts at column N (zero-indexed)
    currency_in_column = {}
    for currency, _ in amounts.items():         # Only uses currencies to set number of headers for the transactions
        
        # Define in and out columns
        in_column = column
        out_column = column + 1
        
        # Write headers of currency and "In" and "Out" column
        sheet.merge_range(row, in_column, row, out_column, currency, format["merged_header_side_borders"])
        sheet.write(row + 1, in_column, "In", format["center_align_left_and_bottom_borders"])
        sheet.write(row + 1, out_column, "Out", format["center_align_right_and_bottom_borders"])
        
        # Write formula of "SUM Total" column
        total_sum_formula = "=" + column_index[in_column] + str(row + 4) + "-" + column_index[out_column] + str(row + 4)
        sheet.merge_range(row + 2, in_column, row + 2, out_column, total_sum_formula, format["merged_header_full_border"])
        
        # Write formula of "In" and "Out" column
        sum_formula_in = "=SUM(" + column_index[in_column] + str(row + 5) + ":" + column_index[in_column] + str(row + 4 + number_of_transactions) + ")"
        sum_formula_out = "=SUM(" + column_index[out_column] + str(row + 5) + ":" + column_index[out_column] + str(row + 4 + number_of_transactions) + ")"
        sheet.write(row + 3, in_column, sum_formula_in, format["center_align_left_and_bottom_borders"])
        sheet.write(row + 3, out_column, sum_formula_out, format["center_align_right_and_bottom_borders"])
        
        # Update currency_column
        currency_in_column[currency] = in_column
        
        column += 2


    # Update assets per transaction
    row = 8         # Starts at row 8
    column = 13     # Starts at column N
    for transaction in transactions:
        
        # Get column of currency bought and sold
        in_column = currency_in_column[transaction[transaction_index["currency_bought"]]]
        out_column = currency_in_column[transaction[transaction_index["currency_sold"]]] + 1
        
        # Get cells of transaction
        cell_date = column_index[column] + str(row)
        cell_currency_bought = column_index[in_column] + str(row)
        cell_currency_sold = column_index[out_column] + str(row)
        
        # Write date, amount bought and amount sold of transaction
        sheet.write(cell_date, transaction[transaction_index["date"]].strftime("%Y-%m-%d"), format["right_border"])
        sheet.write(cell_currency_bought, transaction[transaction_index["amount_bought"]], format["center_align"])
        sheet.write(cell_currency_sold, transaction[transaction_index["amount_sold"]], format["center_align"])
        
        row += 1
        
    # TODO: Format left border at all bought columns, and right border at all sold columns, for all transactions
        
    print('Assets sheet completed.') 
    
    return None


### Helper Methods ###
def initialize_workbook_and_worksheets():
    workbook = xlsxwriter.Workbook('tax_info_test.xlsx')
    transactions_sheet = workbook.add_worksheet('Transactions')
    results_sheet = workbook.add_worksheet('Results')
    assets_sheet = workbook.add_worksheet('Assets')
    
    return workbook, transactions_sheet, results_sheet, assets_sheet

def get_format(workbook):
    
    format = {
        "sheet_header": workbook.add_format({'bold': 1, 'font_size': 14}),
        "sheet_subheader": workbook.add_format({'bold': 1, 'font_size': 12}),
        "column_header": workbook.add_format({'bold': 1, 'bottom': 1}),
        "merged_header_no_borders": workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_right_border": workbook.add_format({'bold': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_left_border": workbook.add_format({'bold': 1, 'left': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_side_borders": workbook.add_format({'bold': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_bottom_border": workbook.add_format({'bold': 1, 'bottom': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_top_border": workbook.add_format({'bold': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_left_right_and_bottom_borders": workbook.add_format({'bold': 1, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_left_right_and_top_borders": workbook.add_format({'bold': 1, 'left': 1, 'right': 1, 'top': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_full_border": workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merged_header_left_align": workbook.add_format({'bold': 1, 'align': 'left', 'valign': 'vcenter'}),
        "merged_header_left_align_bottom_border": workbook.add_format({'bold': 1, 'bottom': 1, 'align': 'left', 'valign': 'vcenter'}),
        "center_align": workbook.add_format({'align': 'center'}),
        "center_align_percentage": workbook.add_format({'align': 'center', 'num_format': '0.00%'}),
        "center_align_left_border": workbook.add_format({'align': 'center', 'left': 1}),
        "center_align_right_border": workbook.add_format({'align': 'center', 'right': 1}),
        "center_align_side_borders": workbook.add_format({'align': 'center', 'left': 1, 'right': 1}),
        "center_align_bottom_border": workbook.add_format({'align': 'center', 'bottom': 1}),
        "center_align_top_border": workbook.add_format({'align': 'center', 'top': 1}),
        "center_align_left_and_bottom_borders": workbook.add_format({'align': 'center', 'left': 1, 'bottom': 1}),
        "center_align_right_and_bottom_borders": workbook.add_format({'align': 'center', 'right': 1, 'bottom': 1}),
        "center_align_left_and_top_borders": workbook.add_format({'align': 'center', 'left': 1, 'top': 1}),
        "center_align_right_and_top_borders": workbook.add_format({'align': 'center', 'right': 1, 'top': 1}),
        "left_border": workbook.add_format({'left': 1}),
        "right_border": workbook.add_format({'right': 1}),
        "green": workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'}),
        "red": workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    }

    return format

def get_bar_chart(workbook):
    
    return workbook.add_chart({'type': 'bar'})

def get_pie_chart(workbook):
    
    return workbook.add_chart({'type': 'pie'})

def get_transaction_index():
    
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
    
    return transaction_index

def get_amount_index():
    
    # Define amounts
    amount_index = {
        "date": 0,
        "amount": 1
    }

    return amount_index

def get_column_index():
    
    # Define column index of sheet
    column_index = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "J",
        10: "K",
        11: "L",
        12: "M",
        13: "N",
        14: "O",
        15: "P",
        16: "Q",
        17: "R",
        18: "S",
        19: "T",
        20: "U",
        21: "V",
        22: "W",
        23: "X",
        24: "Y",
        25: "Z"
    }
    
    return column_index

def get_orders():
    
    # Define orders
    orders = {
        "FIFO": Queue(),
        "LIFO": Stack()
    }
    
    return orders

def get_unique_currencies(transactions):
    
    transaction_index = get_transaction_index()
    
    # Find unique currencies
    unique_currencies = set()
    for transaction in transactions:
        if transaction[transaction_index["currency_sold"]] not in unique_currencies: unique_currencies.add(transaction_index["currency_sold"])
        if transaction[transaction_index["currency_bought"]] not in unique_currencies: unique_currencies.add(transaction_index["currency_bought"])

    return unique_currencies


### Testing ###

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = ["2022-11-12", "USD", 1000, 1, "BTC", 1, 1000]
cleaned_transaction_2 = ["2022-11-15", "BTC", 0.25, 1200, "USD", 300, 1]
cleaned_transaction_3 = ["2022-11-18", "USD", 750, 1, "BTC", 0.5, 1500]
cleaned_transaction_4 = ["2022-11-22", "USD", 500, 1, "ETH", 5, 100]
cleaned_transaction_5 = ["2022-11-27", "USD", 200, 1, "LTC", 4, 50]
cleaned_transaction_6 = ["2022-12-05", "ETH", 2.5, 80, "USD", 200, 1]
cleaned_transactions = [
    cleaned_transaction_1,
    cleaned_transaction_2,
    cleaned_transaction_3,
    cleaned_transaction_4,
    cleaned_transaction_5,
    cleaned_transaction_6
]

# Amounts
amounts = {"BTC": Stack(), "ETH": Stack(), "LTC": Stack(), "USD": Stack()}
amounts["BTC"].enqueue(["2022-11-15", 0.75])
amounts["BTC"].enqueue(["2022-11-18", 0.5])
amounts["ETH"].enqueue(["2022-11-22", 2.5])
amounts["LTC"].enqueue(["2022-11-27", 4])
amounts["USD"].enqueue(["2022-12-05", 0])           # TODO: Handle fiat amounts (can't be negative (-1950))

# Profits
transaction_profits = [0, 50, 0, 0, 0, -50]
currency_transaction_profits = {"BTC": ["2022-11-15", 50], "ETH": ["2022-12-05", -30]}
currency_profits = {"BTC": 50, "ETH": -30}          # LTC profit never realized. Not stored in currency_profits

# write_to_excel(cleaned_transactions, amounts, transaction_profits, currency_transaction_profits, currency_profits)





