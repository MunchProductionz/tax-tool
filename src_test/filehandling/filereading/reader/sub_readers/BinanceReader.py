import pandas as pd

# BinanceReader
class BinanceReader:

    def __init__(self):
        self.time_format = self.get_time_format()

    def read_file(self, file_path):
        
        time_format = self.time_format
        
        # Excel
        uncleaned_data = pd.read_excel(r'' + file_path + '')
        cleaned_data = uncleaned_data[["Date", "Market", "Type", "Price", "Amount", "Total"]]
        
        transactions = []
        
        for row in range(len(cleaned_data)):
            date = cleaned_data["Date"].loc[row]
            date_formatted = date.strftime(time_format)
            type = cleaned_data["Type"].loc[row]
            market = cleaned_data["Market"].loc[row]
            first_currency = self.get_first_currency(market)
            second_currency = market[len(first_currency):]
            
            if type == 'SELL':
                currency_sold = first_currency
                price_sold = cleaned_data["Price"].loc[row]
                amount_sold = cleaned_data["Amount"].loc[row]
                
                currency_bought = second_currency
                price_bought = 1 / price_sold
                amount_bought = cleaned_data["Total"].loc[row]
            else:
                currency_bought = first_currency
                price_bought = cleaned_data["Price"].loc[row]
                amount_bought = cleaned_data["Total"].loc[row]
                
                currency_sold = second_currency
                price_sold = 1 / price_bought
                amount_sold = cleaned_data["Amount"].loc[row]
            
            transaction = [date_formatted, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
            transactions.append(transaction)
        
        return transactions
    
    
    ## Help methods ##
    def get_first_currency(self, market):
    
        currencies = self.get_currencies()
        first_currency = None
        
        for ticker in range(1, len(market)-1):
            if market[:ticker] in currencies:
                first_currency = market[:ticker]
        
        return first_currency    # TODO: Handle when ticker is invalid
    
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