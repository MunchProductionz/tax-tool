



def get_price(date, currency, fiat):

    # Get fiat_price of currency on input date

    # Placeholder implementation
    
    currencies = {
        "BTC": 10000,
        "ETH": 400,
        "LTC": 50,
        "USD": 1
    }
    
    if currency in currencies.keys():
        fiat_price = currencies[currency]
    else:
        fiat_price = 10

    return fiat_price