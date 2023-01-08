from rest.calculations.datastructures import Queue
from rest.calculations.datastructures import Stack
from rest.calculations.priceretriever import get_price

#Steg:
# - X Finn unike currencies
# - X Initialiser datastrukterer for antall i beholdning per currency
# - X Legg datastrukterer til i dictionary for antall
# - X Initialiser variabler for profitt per currency
# - X Legg datastrukterer til i dictionary for profitt
# - Utfør utregninger
# -- / Hent priser
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

    # Define transaction
    index_date = 0
    index_currency_sold = 1
    index_amount_sold = 2
    index_price_sold = 3
    index_currency_bought = 4
    index_amount_bought = 5
    index_price_bought = 6

    # Find unique currencies
    unique_currencies = set()
    for transaction in transactions:
        if transaction[index_currency_sold] not in unique_currencies: unique_currencies.add(transaction[index_currency_sold])
        if transaction[index_currency_bought] not in unique_currencies: unique_currencies.add(transaction[index_currency_bought])

    # Initialize dictionaries
    amounts = dict()
    transaction_profits = list()
    currency_transaction_profits = dict()
    currency_profits = dict()

    # Define transaction_profits
    index_transaction_date = 0
    index_transaction_profit = 1

    # Define datastructures
    index_amounts_date = 0
    index_amounts_amount = 1

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
    for transaction in transactions:
        
        date = transaction[index_date]
        currency_sold = transaction[index_currency_sold]
        amount_sold = transaction[index_amount_sold]
        price_sold = transaction[index_price_sold]
        currency_bought = transaction[index_currency_bought]
        amount_bought = transaction[index_amount_bought]
        price_bought = transaction[index_price_bought]

        # Initialize transaction profit of currency sold ([date, transaction_profit])
        transaction_profits.append(0)
        currency_transaction_profits[currency_sold].append[date, 0]
        index_transaction = len(currency_transaction_profits[currency_sold]) - 1

        # Get price of currency sold
        fiat_price_of_currency_sold = get_price(date, currency_sold, fiat)

        # Update amount and profit of currency sold
        temporary_amount_sold = amount_sold
        while temporary_amount_sold > 0:
            
            # Copy stored element amount
            temporary_date_currency_sold, temporary_amount_currency_sold = amounts[currency_sold].dequeue()       # TODO: Handle case when no amount is enqueued before dequeuing
            
            # Get price of stored element
            fiat_price_of_temporary_date_currency_sold = get_price(temporary_date_currency_sold, currency_sold, fiat)
            
            # If stored element amount > sold amount (Base case)
            if temporary_amount_currency_sold >= temporary_amount_sold:
                temporary_amount_currency_sold -= temporary_amount_sold
                cost_bought = temporary_amount_sold * price_sold * fiat_price_of_temporary_date_currency_sold       # TODO: Correct to use price_sold?
                income_sold = temporary_amount_sold * price_sold * fiat_price_of_currency_sold
                element_profit = income_sold - cost_bought
                transaction_profits[counter] += element_profit
                currency_transaction_profits[currency_sold][index_transaction][index_transaction_profit] += element_profit
                currency_profits[currency_sold] += element_profit
                amounts[currency_sold].re_enqueue([temporary_date_currency_sold, temporary_amount_currency_sold])
                temporary_amount_sold = 0
                break

            # If stored element amount < sold amount
            cost_bought = temporary_amount_currency_sold * price_sold * fiat_price_of_temporary_date_currency_sold  # TODO: Correct to use price_sold?
            income_sold = temporary_amount_currency_sold * price_sold * fiat_price_of_currency_sold
            element_profit = income_sold - cost_bought
            currency_transaction_profits[currency_sold][index_transaction][index_transaction_profit] += element_profit
            currency_profits[currency_sold] += element_profit
            temporary_amount_sold -= temporary_amount_currency_sold     # TODO: Fix case where sold amount > stored amount (infinite runs)

        # Update amount of currency bought
        amounts[currency_bought].enqueue([date, amount_bought])
        
        # Update counter
        counter += 1

    return amounts, transaction_profits, currency_transaction_profits, currency_profits



### Helper methods ###

def isValidOrder(order):
    return order == "FIFO" or order == "LIFO"

def isValidFiat(fiat):
    
    valid_fiats = [
        "USD",
        "GBP",
        "NOK"
    ]

    if fiat in valid_fiats:
        return True

    return False