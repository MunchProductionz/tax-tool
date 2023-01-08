#Visualizations:
# - Total profit per currency (Bar chart?)
# - Amounts per currency (Bar chart? Measured in fiat?)
# - Price graph of currency (Line chart?)
# -- Daily chart of a year? (Adjustable?)
# -- Dots on transaction (green = buy, red = sell)
# -- Unrealized/Realized profit on hover
# TODO: Implement

# TODO: Visualize in react app using JavaScript

from readers import get_files
from datacleaner import get_transactions_from_files
from calculation import calculate_profit

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Tax tool API"}

@app.get("/files")
async def get_files_lol():
    files = get_files()
    return files

@app.get("/transactions")
async def get_transactions():
    files = get_files()
    transactions = get_transactions_from_files(files)
    return transactions


@app.get("/profits")
async def get_profits():
    
    order = "FIFO"                      # TODO: User input
    fiat = "USD"                        # TODO: User input

    files = get_files()
    transactions = get_transactions_from_files(files)
    amounts, transaction_profits, currency_transaction_profits, currency_profits = calculate_profit(transactions, order, fiat)

    return {
        "amounts": amounts,
        "transaction_profits": transaction_profits,
        "currency_transaction_profits": currency_transaction_profits,
        "currency_profits": currency_profits
    }