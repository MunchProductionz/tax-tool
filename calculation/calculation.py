from datastructures import Queue
from datastructures import Stack
from priceretriever import get_price
from variables import isValidFiat

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

        # Get price of currency sold
        fiat_price_of_currency_sold = get_price(date, currency_sold, fiat)

        # Update amount and profit of currency sold
        temporary_amount_sold = amount_sold
        while temporary_amount_sold > 0:
            
            # Copy stored element amount and get price of stored element
            if amounts[currency_sold].isEmpty(): 
                fiat_price_of_temporary_date_currency_sold = 0
                temporary_amount_currency_sold = 0
                cost_bought = temporary_amount_currency_sold * price_sold * fiat_price_of_temporary_date_currency_sold  # TODO: Correct to use price_sold?
                income_sold = temporary_amount_sold * price_sold * fiat_price_of_currency_sold
                element_profit = income_sold - cost_bought
                transaction_profits[counter] += element_profit
                currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += element_profit
                currency_profits[currency_sold] += element_profit
                break
            else:
                temporary_date_currency_sold, temporary_amount_currency_sold = amounts[currency_sold].dequeue()       # TODO: Handle case when no amount is enqueued before dequeuing
                fiat_price_of_temporary_date_currency_sold = get_price(temporary_date_currency_sold, currency_sold, fiat)
            
            # If stored element amount > sold amount (Base case)
            if temporary_amount_currency_sold >= temporary_amount_sold:
                temporary_amount_currency_sold -= temporary_amount_sold
                cost_bought = temporary_amount_sold * price_sold * fiat_price_of_temporary_date_currency_sold       # TODO: Correct to use price_sold?
                income_sold = temporary_amount_sold * price_sold * fiat_price_of_currency_sold
                element_profit = income_sold - cost_bought
                transaction_profits[counter] += element_profit
                currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += element_profit
                currency_profits[currency_sold] += element_profit
                amounts[currency_sold].re_enqueue([temporary_date_currency_sold, temporary_amount_currency_sold])
                temporary_amount_sold = 0
                break

            # If stored element amount < sold amount
            cost_bought = temporary_amount_currency_sold * price_sold * fiat_price_of_temporary_date_currency_sold  # TODO: Correct to use price_sold?
            income_sold = temporary_amount_currency_sold * price_sold * fiat_price_of_currency_sold
            element_profit = income_sold - cost_bought
            transaction_profits[counter] += element_profit
            currency_transaction_profits[currency_sold][index_transaction][transaction_profits_index["profit"]] += element_profit
            currency_profits[currency_sold] += element_profit
            temporary_amount_sold -= temporary_amount_currency_sold

        # Update amount of currency bought
        amounts[currency_bought].enqueue([date, amount_bought])
        
        # Update counter
        counter += 1
        counter_transactions_completed += 1
        
        print('Transaction ' + str(counter) + ' completed.')
    
    
    print('# of transactions completed: ' + str(counter_transactions_completed))
    print('# of transactions dropped: ' + str(counter_transactions_dropped))
    print('# of transaction in total: ' + str(counter))

    return amounts, transaction_profits, currency_transaction_profits, currency_profits



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

# Transactions: [transaction1, transaction2, ...]
# Transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
transaction_1 = ["2022-11-12", "USD", 1000, 1, "BTC", 1, 1000]
transaction_2 = ["2022-11-15", "BTC", 0.25, 1200, "USD", 300, 1]
transaction_3 = ["2022-11-18", "USD", 750, 1, "BTC", 0.5, 1500]
transaction_4 = ["2022-11-22", "USD", 500, 1, "ETH", 5, 100]
transaction_5 = ["2022-11-27", "USD", 200, 1, "LTC", 4, 50]
transaction_6 = ["2022-12-05", "ETH", 2.5, 80, "USD", 200, 1]
transactions = [
    transaction_1,
    transaction_2,
    transaction_3,
    transaction_4,
    transaction_5,
    transaction_6
]

order = 'FIFO'
fiat = 'NOK'



# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = ["2022-11-12", "USD", 16939.105, 1, "BTC", 1, 16939.105]    # Added actual average price sold/bought
cleaned_transaction_2 = ["2022-11-15", "BTC", 0.25, 16768.18, "USD", 4192.045, 1]   # Added actual average price sold/bought
cleaned_transaction_3 = ["2022-11-18", "USD", 8356.345, 1, "BTC", 0.5, 16712.69]    # Added actual average price sold/bought
cleaned_transaction_4 = ["2022-11-22", "USD", 5613.675, 1, "ETH", 5, 1122.735]      # Added actual average price sold/bought
cleaned_transaction_5 = ["2022-11-27", "USD", 302.7, 1, "LTC", 4, 75.675]           # Added actual average price sold/bought
cleaned_transaction_6 = ["2022-12-05", "ETH", 2.5, 1271.09, "USD", 3177.725, 1]     # Added actual average price sold/bought
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
transaction_currency_profits = {"BTC": ["2022-11-15", 50], "ETH": ["2022-12-05", -30]}
currency_profits = {"BTC": 50, "ETH": -30}          # LTC profit never realized. Not stored in currency_profits



calculate_profit(transactions, order, fiat)