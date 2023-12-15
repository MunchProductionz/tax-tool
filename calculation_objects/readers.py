import glob
import pandas as pd


class FileReader:
    
    # Get uploaded files
    def get_files(self):

        # TODO: Create method for storing files
        # TODO: Separate between different exchanges
        # TODO: Handle case when file is not valid type

        # Create lists of uploaded files
        files = list()          # TODO: Rewrite to use dictionary with lists instead of 2D-list
        
        # Get valid exchanges
        exchanges = ExchangeReaders().get_exchanges()

        # Add uploaded files' file_path and their exchanges to files
        for exchange in exchanges:
            for file_path in glob.glob("../files/*" + exchange + "*"):
                files.append([exchange, file_path])

        return files
    
    

# Contains all exchange readers
class ExchangeReaders:
    
     # Get reader
    def get_reader(self, exchange):

        # Get readers
        readers = self.get_readers()

        # Validations
        if not self.isValidExchange(exchange): return None                       # TODO: Fix error handling

        return readers[exchange]

    def read_file(self, reader, file_path):

        # Use reader to read filedata
        transactions = reader.read_file(file_path)

        return transactions

    ## Help methods ##
    def isValidExchange(self, exchange):
        
        readers = self.get_readers()
        
        for reader_exchange in readers:
            if exchange == reader_exchange: return True
        return False
    
    def get_exchanges(self):
        
        exchanges = [
            "Binance",
            "Coinbase"
        ]
        
        return exchanges

    def get_readers(self):
        
        readers = {
            "Binance": BinanceReader(),
            "Coinbase": CoinbaseReader()
        }
        
        return readers




# BinanceReader
class BinanceReader:

    def read_file(self, file_path):
        
        time_format = self.get_time_format()
        
        # Excel
        # uncleaned_data = pd.read_excel(filedata)      # TODO: Implement if possible to input file
        uncleaned_data = pd.read_excel(r'' + file_path + '')
        cleaned_data = uncleaned_data[["Date", "Market", "Type", "Price", "Amount", "Total"]]
        
        print(cleaned_data.head())
        
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

        # Read filedata
        # Put data into transactions-format
        # Return transactions
        
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
    
    

# CoinbaseReader
class CoinbaseReader:

    def read_file(self, file_path):
        
        time_format = self.get_time_format()
        number_of_rows_skipped = 7
        
        print("YOOOOO")
        
        # TODO: Implement regex (optional) to remove " " around rows. (Can't read CSV with open())
        # TODO: Verify with updated testfile that formatting is correct.
        
        # CSV
        uncleaned_data = pd.read_csv(r'' + file_path + '', delimiter=',', quotechar='"', skiprows=number_of_rows_skipped)
        
        print(uncleaned_data.head())
        print("BROOOO")
        
        # cleaned_data = uncleaned_data[["Date(UTC)"]]
        cleaned_data = uncleaned_data[["Timestamp", "Transaction Type", "Asset", "Quantity Transacted", "USD Spot Price at Transaction", "USD Subtotal"]]
        
        
        print("CLEANED")
        
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
    
    