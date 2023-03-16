
currencies_full_names = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'LTC': 'Litecoin',
}

days_in_months = {
    '01': '31',
    '02': '28',
    '03': '31',
    '04': '30',
    '05': '31',
    '06': '30',
    '07': '31',
    '08': '31',
    '09': '30',
    '10': '31',
    '11': '30',
    '12': '31'
}

def convert_values_to_lowercase(dictionary):
    currencies_full_names_small_letters = dict()
    
    for ticker, name in dictionary.items():
        currencies_full_names_small_letters[ticker] = name.lower()
        
    return currencies_full_names_small_letters

