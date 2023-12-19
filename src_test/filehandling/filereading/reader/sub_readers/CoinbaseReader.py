import pandas as pd

# CoinbaseReader
class CoinbaseReader:

    def read_file(self, file_path):
        
        time_format = self.get_time_format()
        number_of_rows_skipped = 7
        
        # TODO: Implement regex (optional) to remove " " around rows. (Can't read CSV with open())
        # TODO: Verify with updated testfile that formatting is correct.
        
        # CSV
        uncleaned_data = pd.read_csv(r'' + file_path + '', delimiter=',', quotechar='"', skiprows=number_of_rows_skipped)
        
        # cleaned_data = uncleaned_data[["Date(UTC)"]]
        cleaned_data = uncleaned_data[["Timestamp", "Transaction Type", "Asset", "Quantity Transacted", "USD Spot Price at Transaction", "USD Subtotal"]]
        
        print(cleaned_data.head())
        
        
        transactions = []
        
        for row in range(len(cleaned_data)):
            date = cleaned_data["Date"].loc[row]
            date_formatted = date.strftime(time_format)
            type = cleaned_data["Transaction Type"].loc[row]
            note = cleaned_data["Notes"].loc[row]
            second_currency = self.get_currency_from_end_of_note(note)
            
            if type == 'SELL':
                currency_sold = cleaned_data["Asset"].loc[row]
                price_sold = cleaned_data["USD Spot Price at Transaction"].loc[row]
                amount_sold = cleaned_data["Quantity Transacted"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = self.get_amount_from_end_of_note(note)
            elif type == 'BUY':
                currency_bought = cleaned_data["Asset"].loc[row]
                price_bought = cleaned_data["USD Spot Price at Transaction"].loc[row]
                amount_bought = cleaned_data["Quantity Transacted"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = self.get_amount_from_end_of_note(note)
            else:
                break
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)


        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
        return None
    
    
    ## Help methods ##
    def get_currency_from_end_of_note(self, note):
    
        currencies = self.get_currencies()
        currency = None
        
        for ticker in range(len(note)-1, 1, -1):
            if note[ticker:] in currencies:
                currency = note[ticker:]
        
        return currency    # TODO: Handle when ticker is invalid

    def get_amount_from_end_of_note(self, note):
        
        currency = self.get_currency_from_end_of_note(note)
        amount = 0
        
        for number in range(len(note)-len(currency)-1, 1, -1):
            if note[number:number + 1] == " ":
                amount = int(note[number:len(note)-len(currency)-1])
                
        return amount
    
    def get_currencies(self):
    
        currencies = [
            "BTC",
            "ETH",
            "LTC",
            "XRP",
            "POWR",
            "USD"
        ]

        return currencies
    
    def get_time_format(self):
    
        return '%Y-%m-%d %X'