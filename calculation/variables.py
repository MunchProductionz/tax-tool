### Variables ###

cryptocurrencies_full_names = {
    
    # Cryptocurrencies
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'LTC': 'Litecoin',
    'XRP': 'XRP',
    'POWR': 'Power Ledger',
}

fiat_currencies_full_names = {
    
    # Fiat currencies
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'NOK': 'Norwegian Krone',
    'INR': 'Indian Rupee',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'SGD': 'Singapore Dollar',
    'CHF': 'Swiss Franc',
    'MYR': 'Malaysian Ringgit',
    'JPY': 'Japanese Yen',
    'CNY': 'Chinese Yuan Renminbi',     # Uses RMB for domestic transactions
    'ARS': 'Argentine Peso',
    'BHD': 'Bahraini Dinar',
    'BWP': 'Botswana Pula',
    'BRL': 'Brazilian Real',
    'BND': 'Bruneian Dollar',
    'BGN': 'Bulgarian Lev',
    'CLP': 'Chilean Peso',
    'COP': 'Colombian Peso',
    'CZK': 'Czech Koruna',
    'DKK': 'Danish Krone',
    'AED': 'Emirati Dirham',
    'HKD': 'Hong Kong Dollar',
    'HUF': 'Hungarian Forint',
    'ISK': 'Icelandic Krona',
    'IDR': 'Indonesian Rupiah',
    'IRR': 'Iranian Rial',
    'ILS': 'Israeli Shekel',
    'KZT': 'Kazakhstani Tenge',
    'KWD': 'Kuwaiti Dinar',
    'LYD': 'Libyan Dinar',
    'MUR': 'Mauritian Rupee',
    'MXN': 'Mexican Peso',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PKR': 'Pakistani Rupee',
    'PHP': 'Philippine Peso',
    'PLN': 'Polish Zloty',
    'QAR': 'Qatari Riyal',
    'RON': 'Romanian New Leu',
    'RUB': 'Russian Ruble',
    'SAR': 'Saudi Arabian Riyal',
    'ZAR': 'South African Rand',
    'KRW': 'South Korean Won',
    'LKR': 'Sri Lankan Rupee',
    'SEK': 'Swedish Krona',
    'TWD': 'Taiwan New Dollar',
    'THB': 'Thai Baht',
    'TTD': 'Trinidadian Dollar',
    'TRY': 'Turkish Lira',
    'VEF': 'Venezuelan Bolivar'
    
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


### Methods ###

def convert_values_to_lowercase(dictionary):
    currencies_full_names_small_letters = dict()
    
    for ticker, name in dictionary.items():
        currencies_full_names_small_letters[ticker] = name.lower()
        
    return currencies_full_names_small_letters

def isValidCurrency(currency):
    if currency in cryptocurrencies_full_names:
        return True
    if currency in fiat_currencies_full_names:
        return True
    return False

def isValidFiat(currency):
    if isUSDollar(currency):
        return True
    if isFiat(currency):
        return True
    return False

def isUSDollar(currency):
    if currency == 'USD':
        return True
    return False

def isFiat(currency):
    if not isUSDollar(currency):
        if currency in fiat_currencies_full_names:
            return True
    return False