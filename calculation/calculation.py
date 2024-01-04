from datastructures import Queue
from datastructures import Stack
from priceretriever import get_price
from variables import isValidFiat
from datetime import datetime

#Steg:
# - X Finn unike currencies
# - X Initialiser datastrukterer for antall i beholdning per currency
# - X Legg datastrukterer til i dictionary for antall
# - X Initialiser variabler for profitt per currency
# - X Legg datastrukterer til i dictionary for profitt
# - Utfør utregninger
# -- X Hent priser
# -- X Hent antall i beholdning av salgscurrency
# --- X Hvis beholdningsantall >= salgsantall: bruk av beholdningsantall (oppdater element)
# --- X Hvis beholdningsantall < salgsantall: bruk opp og gå videre til neste antall til condition over stemmer
# -- X Legg til antall i beholdning av kjøpscurrency
# -- X Regn realisert profitt ved handelstidspunkt
# -- X Legg realisert profitt til dictionary for profitt

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# TODO: USD, NOK, etc. are valid currencies (handle these cases)
# TODO: Allow user to choose wanted fiat conversion

def calculate_profit(transactions, order, fiat):

    # Validations
    if not isValidOrder(order): raise ValueError("Invalid order.")          # TODO: Test error handling
    if not isValidFiat(fiat): raise ValueError("Invalid fiat.")             # TODO: Test error handling

    # Define indexes
    transaction_index = get_transaction_index()
    transaction_profits_index = get_transaction_profits_index()
    amounts_index = get_amounts_index()

    # Find unique currencies
    unique_currencies = set()
    for transaction in transactions:
        if transaction == None: continue # Made to prevent NoneType is not subscriptable error
        if transaction[transaction_index["currency_sold"]] not in unique_currencies: unique_currencies.add(transaction[transaction_index["currency_sold"]])
        if transaction[transaction_index["currency_bought"]] not in unique_currencies: unique_currencies.add(transaction[transaction_index["currency_bought"]])

    # Initialize dictionaries
    amounts = dict()
    amounts_history = dict()
    transaction_profits = list()
    currency_transaction_profits = dict()
    currency_profits = dict()

    # TODO: Append lists [amount, date] to datastructure
    # Define orders
    orders = {
        "FIFO": Queue(),
        "LIFO": Stack()
    }

    # Initialize datastructures and variables
    for currency in unique_currencies:
        amounts[currency] = orders[order]
        currency_transaction_profits[currency] = []
        currency_profits[currency] = 0
        amounts_history[currency] = []

    # Make calculation per transaction
    counter = 0
    counter_transactions_dropped = 0
    counter_transactions_completed = 0
    for transaction in transactions:
        if transaction == None: 
            counter += 1
            counter_transactions_dropped += 1
            print('Transaction ' + str(counter) + ' was dropped (Transaction == None).')
            continue # Made to prevent NoneType is not subscriptable error
        else:
            date = transaction[transaction_index["date"]]
            currency_sold = transaction[transaction_index["currency_sold"]]
            amount_sold = transaction[transaction_index["amount_sold"]]
            price_sold = transaction[transaction_index["price_sold"]]
            currency_bought = transaction[transaction_index["currency_bought"]]
            amount_bought = transaction[transaction_index["amount_bought"]]
            price_bought = transaction[transaction_index["price_bought"]]

            # Initialize transaction profit of currency sold ([date, transaction_profit])
            transaction_profits.append(0)
            if currency_transaction_profits[currency_sold] == None:
                currency_transaction_profits[currency_sold] = [[date, 0]]
            else:
                currency_transaction_profits[currency_sold].append([date, 0])
                
            # Define index of last transaction in transaction_profits
            index_transaction = len(currency_transaction_profits[currency_sold]) - 1

            # Get price of currency sold and bought
            fiat_price_of_currency_sold = get_price(date, currency_sold, fiat)
            fiat_price_of_currency_bought = get_price(date, currency_bought, fiat)
            
            print()
            print(f'Currency sold: {currency_sold} - Amount sold: {amount_sold} - Fiat price of currency sold: {fiat_price_of_currency_sold}')
            print(f'Currency bought: {currency_bought} - Amount bought: {amount_bought} - Fiat price of currency bought: {fiat_price_of_currency_bought}')

            # Update amount and profit of currency sold
            temporary_amount_sold = amount_sold
            while temporary_amount_sold > 0:
                
                # TODO: Move into help methods?
                
                # Copy stored element amount and get price of stored element
                # TODO: Need to handle case where asset with amount 0 is sold
                if amounts[currency_sold].isEmpty(): 
                    fiat_cost_bought = 0
                    fiat_income_sold = temporary_amount_sold * fiat_price_of_currency_sold          # Assumes amount sold is 100% profit
                    # fiat_income_sold = 0                                                                             # TODO: Account for profits of initial buying currency (either as a negative or as an existing asset input from the user)                           
                    fiat_element_profit = fiat_income_sold - fiat_cost_bought                                                  # TODO: Make sure there are either no profits from initial buying currency, or it is accounted for (either as a negative or as an existing asset input by the user)
                    transaction_profits[counter] += fiat_element_profit
                    currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += fiat_element_profit   # TODO: Handle that these are 0
                    currency_profits[currency_sold] += fiat_element_profit
                    temporary_amount_sold = 0       # Stops the while loop
                else:
                    temporary_date_currency_sold, temporary_amount_currency_sold, fiat_price_of_temporary_date_currency_sold = amounts[currency_sold].dequeue()       # TODO: Handle case when no amount is enqueued before dequeuing (NOTE: should be fixed by the if statement above)
                
                    # If stored element amount > sold amount (Base case)
                    if temporary_amount_currency_sold >= temporary_amount_sold:
                        temporary_amount_currency_sold -= temporary_amount_sold
                        fiat_cost_bought = temporary_amount_sold * fiat_price_of_temporary_date_currency_sold
                        fiat_income_sold = temporary_amount_sold * fiat_price_of_currency_sold
                        fiat_element_profit = fiat_income_sold - fiat_cost_bought
                        transaction_profits[counter] += fiat_element_profit
                        currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += fiat_element_profit
                        currency_profits[currency_sold] += fiat_element_profit
                        updated_amount_currency_sold = temporary_amount_currency_sold - temporary_amount_sold
                        if updated_amount_currency_sold > 0:
                            amounts[currency_sold].re_enqueue([temporary_date_currency_sold, updated_amount_currency_sold, fiat_price_of_temporary_date_currency_sold])
                        temporary_amount_sold = 0       # Stops the while loop
                    else:
                        # If stored element amount < sold amount
                        fiat_cost_bought = temporary_amount_currency_sold * fiat_price_of_temporary_date_currency_sold
                        fiat_income_sold = temporary_amount_currency_sold * fiat_price_of_currency_sold
                        fiat_element_profit = fiat_income_sold - fiat_cost_bought
                        transaction_profits[counter] += fiat_element_profit
                        currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += fiat_element_profit
                        currency_profits[currency_sold] += fiat_element_profit
                        temporary_amount_sold -= temporary_amount_currency_sold
    
            # Update amount of currency bought
            amounts[currency_bought].enqueue([date, amount_bought, fiat_price_of_currency_bought])
            
            # Find value of transaction of currency sold and bought
            fiat_value_currency_sold = amount_sold * -fiat_price_of_currency_sold
            fiat_value_currency_bought = amount_bought * fiat_price_of_currency_bought
            
            # Update amounts_history of currency sold and bought
            amounts_history[currency_sold].append([date, amount_sold, -fiat_price_of_currency_sold, fiat_value_currency_sold])
            amounts_history[currency_bought].append([date, amount_bought, fiat_price_of_currency_bought, fiat_value_currency_bought])
            
            # Update counter
            counter += 1
            counter_transactions_completed += 1
            
            print('Transaction ' + str(counter) + ' completed.')
    
    
    print('# of transactions completed: ' + str(counter_transactions_completed))
    print('# of transactions dropped: ' + str(counter_transactions_dropped))
    print('# of transaction in total: ' + str(counter))
    print()

    print('Amounts:')
    print(amounts)
    print()
    print('Transaction profits:')
    print(currency_transaction_profits)
    print()
    print('Currency profits:')
    print(currency_profits)
    print()
    print('Amounts history:')
    print(amounts_history)
    print()

    return amounts, transaction_profits, currency_transaction_profits, currency_profits, amounts_history



### Helper methods ###

def isValidOrder(order):
    return order == "FIFO" or order == "LIFO"

def get_transaction_index():
    
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

def get_transaction_profits_index():
    
    transaction_profits_index = {
        "date": 0,
        "profit": 1
    }
    
    return transaction_profits_index

def get_amounts_index():
    
    amounts_index = {
        "date": 0,
        "amount": 1
    }
    
    return amounts_index


### Testing ###
date_format = "%Y-%m-%d"
date_1 = datetime.strptime("2022-11-12", date_format)
date_2 = datetime.strptime("2022-11-15", date_format)
date_3 = datetime.strptime("2022-11-18", date_format)
date_4 = datetime.strptime("2022-11-22", date_format)
date_5 = datetime.strptime("2022-11-27", date_format)
date_6 = datetime.strptime("2022-12-05", date_format)
date_7 = datetime.strptime("2022-12-20", date_format)


# Transactions: [transaction1, transaction2, ...]
# Transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
transaction_1 = [date_1, "USD", 1000, 1, "BTC", 1, 1000]
transaction_2 = [date_2, "BTC", 0.25, 1200, "USD", 300, 1]
transaction_3 = [date_3, "USD", 750, 1, "BTC", 0.5, 1500]
transaction_4 = [date_4, "USD", 500, 1, "ETH", 5, 100]
transaction_5 = [date_5, "USD", 200, 1, "LTC", 4, 50]
transaction_6 = [date_6, "ETH", 2.5, 80, "USD", 200, 1]
transactions = [
    transaction_1,
    transaction_2,
    transaction_3,
    transaction_4,
    transaction_5,
    transaction_6
]

order = 'FIFO'
fiat = 'USD'



# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = [date_1, "USD", 16939.105, 1, "BTC", 1, 16939.105]    # Added actual average price sold/bought
cleaned_transaction_2 = [date_2, "BTC", 0.25, 16768.18, "USD", 4192.045, 1]   # Added actual average price sold/bought
cleaned_transaction_3 = [date_3, "USD", 8356.345, 1, "BTC", 0.5, 16712.69]    # Added actual average price sold/bought
cleaned_transaction_4 = [date_4, "USD", 5613.675, 1, "ETH", 5, 1122.735]      # Added actual average price sold/bought
cleaned_transaction_5 = [date_5, "USD", 302.7, 1, "LTC", 4, 75.675]           # Added actual average price sold/bought
cleaned_transaction_6 = [date_6, "ETH", 2.5, 1271.09, "USD", 3177.725, 1]     # Added actual average price sold/bought
cleaned_transaction_7 = [date_7, "BTC", 1, 16660.945, "ETH", 13.97214534903220, 1192.44]     # Added actual average price sold/bought

cleaned_transactions = [
    cleaned_transaction_1,
    cleaned_transaction_2,
    cleaned_transaction_3,
    cleaned_transaction_4,
    cleaned_transaction_5,
    cleaned_transaction_6,
    cleaned_transaction_7
]

# Amounts (amounts[currency] = Queue([date_bought, remaining_amount, fiat_price_bought], ...))
amounts = {"BTC": Queue(), "ETH": Queue(), "LTC": Queue(), "USD": Queue()}
amounts["USD"].enqueue(["2022-11-12", -16939.105, 9.933868])  # No negative amounts
amounts["BTC"].enqueue(["2022-11-12", 1, 168270.83310814])
amounts["BTC"].dequeue()
amounts["BTC"].re_enqueue(["2022-11-12", 0.75, 168270.83310814])
amounts["USD"].enqueue(["2022-11-15", 4192.045, 9.966489])
amounts["USD"].enqueue(["2022-11-18", -8356.345, 10.1838640])   # No negative amounts
amounts["BTC"].enqueue(["2022-11-18", 0.5, 170199.76203416])
amounts["USD"].enqueue(["2022-11-22", -5613.675, 10.147814])   # No negative amounts
amounts["ETH"].enqueue(["2022-11-22", 5, 11393.30595129])
amounts["USD"].enqueue(["2022-11-27", -302.7, 9.883106])      # No negative amounts
amounts["LTC"].enqueue(["2022-11-27", 4, 747.90404655])
amounts["ETH"].dequeue()
amounts["ETH"].re_enqueue(["2022-11-22", 2.5, 11393.30595129])
amounts["USD"].enqueue(["2022-12-05", 3177.725, 9.945553])
amounts["BTC"].dequeue()
amounts["BTC"].dequeue()
amounts["BTC"].re_enqueue(["2022-11-18", 0.25, 170199.76203416])
amounts["ETH"].enqueue(["2022-12-20", 13.97214534903220, 11799.7959822])
# TODO: Handle fiat amounts (can't be negative (-1950), not enqueue negative amounts)
# TODO: Check if amounts[currency] is empty (Stack().isEmpty()). If yes, enqueue negative amount. If no, go as usual.

# Profits
transaction_profits = [0, -287.737897030012, 0, 0, 0, 3120.9675287, -3884.60078742004]
transaction_currency_profits = {"BTC": [["2022-11-15", -287.737897030012], ["2022-12-20", -3884.60078742004]], "ETH": ["2022-12-05", 3120.9675287]}
currency_profits = {"BTC": -4172.33868445005, "ETH": 3120.9675287}          # LTC profit never realized. Not stored in currency_profits

# Amounts history (amounts_history[currency] = [[date_transaction, amount_transaction_signed, fiat_price, fiat_value_signed]])
amounts_history = {"USD": [], "BTC": [], "ETH": [], "LTC": []}
amounts_history["USD"].append(["2022-11-12", -16939.105, 9.933868, -168270.83310814])  
amounts_history["BTC"].append(["2022-11-12", 1, 168270.83310814, 168270.83310814])
amounts_history["BTC"].append(["2022-11-15", -0.25, 167119.88152002, -41779.970380005])
amounts_history["USD"].append(["2022-11-15", 4192.045, 9.966489, 41779.970380005])
amounts_history["USD"].append(["2022-11-18", -8356.345, 10.1838640, -85099.88101708])   
amounts_history["BTC"].append(["2022-11-18", 0.5, 170199.76203416, 85099.88101708])
amounts_history["USD"].append(["2022-11-22", -5613.675, 10.147814, -56966.52975645])  
amounts_history["ETH"].append(["2022-11-22", 5, 11393.30595129, 56966.52975645])
amounts_history["USD"].append(["2022-11-27", -302.7, 9.883106, -2991.6161862])     
amounts_history["LTC"].append(["2022-11-27", 4, 747.90404655, 2991.6161862])
amounts_history["ETH"].append(["2022-12-05", -2.5, 12641.69296277, -31604.232406925])
amounts_history["USD"].append(["2022-12-05", 3177.725, 9.945553, 31604.232406925])
amounts_history["BTC"].append(["2022-12-20", -1, 164868.464552225, -164868.464552225])
amounts_history["ETH"].append(["2022-12-20", 13.97214534903220, 11799.7959822, 164868.464552225])


# calculate_profit(transactions, order, fiat)
# calculate_profit(cleaned_transactions, order, fiat)