from price_retriever import PriceRetriever
from datastructures import Queue, Stack

class ProfitCalculator:
    
    def calculate_profit(self, transactions, order, fiat):

        # Validations
        if not self.isValidOrder(order): raise ValueError("Invalid order.")          # TODO: Test error handling
        if not self.isValidFiat(fiat): raise ValueError("Invalid fiat.")             # TODO: Test error handling

        # Define indexes
        transaction_index = self.get_transaction_index()
        transaction_profits_index = self.get_transaction_profits_index()
        amounts_index = self.get_amounts_index()

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
                fiat_price_of_currency_sold = PriceRetriever().get_price(date, currency_sold, fiat)
                fiat_price_of_currency_bought = PriceRetriever().get_price(date, currency_bought, fiat)

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

        return amounts, transaction_profits, currency_transaction_profits, currency_profits, amounts_history



    ### Helper methods ###

    def isValidOrder(self, order):
        return order == "FIFO" or order == "LIFO"

    def get_transaction_index(self):
        
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

    def get_transaction_profits_index(self):
        
        transaction_profits_index = {
            "date": 0,
            "profit": 1
        }
        
        return transaction_profits_index

    def get_amounts_index(self):
        
        amounts_index = {
            "date": 0,
            "amount": 1
        }
        
        return amounts_index