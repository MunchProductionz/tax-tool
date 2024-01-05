import pandas as pd
from io import StringIO
from datetime import datetime

# CoinbaseReader
class CoinbaseReader:

    def __init__(self):
        self.currencies = self.get_currencies()
        self.time_format = self.get_time_format()

    def read_file(self, file_path):
        
        time_format = self.time_format
        number_of_rows_skipped = 7

        cleaned_string_buffer = self.get_cleaned_string_buffer(file_path, number_of_rows_skipped=number_of_rows_skipped)
        data = pd.read_csv(cleaned_string_buffer)
        
        transactions = []
        
        for row in range(len(data)):
            date = data["Timestamp"].loc[row]
            date_formatted = datetime.strptime(date, time_format)
            transaction_type = data["Transaction Type"].loc[row]
            note = data["Notes"].loc[row]
            second_currency = self.get_currency_from_end_of_note(note)
            
            if transaction_type == 'Sell':
                currency_sold = data["Asset"].loc[row]
                price_sold = data["Spot Price at Transaction"].loc[row]
                amount_sold = data["Quantity Transacted"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = self.get_amount_from_end_of_note(note)
            elif transaction_type == 'Buy':
                currency_bought = data["Asset"].loc[row]
                price_bought = data["Spot Price at Transaction"].loc[row]
                amount_bought = data["Quantity Transacted"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = self.get_amount_from_end_of_note(note)
            else:
                # Ignore 'Send' and 'Receive'
                continue
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)
        
        return transactions
    
    
    ## Help methods ##
    
    def get_cleaned_string_buffer(self, file_path, number_of_rows_skipped=7):
        
        processed_lines = []

        with open(file_path, 'r') as file:
            for _ in range(number_of_rows_skipped):
                next(file)

            for line in file:
                if line.startswith('"') and line.endswith('"\n'):
                    line = line[1:-2] + '\n'    # Removes ""
                line = line.replace('""', '"')
                processed_lines.append(line)

        cleaned_data = ''.join(processed_lines)
        cleaned_string_buffer = StringIO(cleaned_data)
        
        return cleaned_string_buffer
        
        
    
    def get_currency_from_end_of_note(self, note):
    
        currencies = self.currencies
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