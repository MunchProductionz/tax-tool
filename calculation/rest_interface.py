#Visualizations:
# - Total profit per currency (Bar chart?)
# - Amounts per currency (Bar chart? Measured in fiat?)
# - Price graph of currency (Line chart?)
# -- Daily chart of a year? (Adjustable?)
# -- Dots on transaction (green = buy, red = sell)
# -- Unrealized/Realized profit on hover
# TODO: Implement

# TODO: Visualize in react app using JavaScript

# from readers import get_files
# from datacleaner import get_transactions_from_files
# from calculation import calculate_profit
from datastructures import Stack

import random
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tax tool API"}

# @app.get("/files")
# async def get_files_lol():
#     files = get_files()
#     return files

# @app.get("/transactions")
# async def get_transactions():
#     files = get_files()
#     transactions = get_transactions_from_files(files)
#     return transactions


# @app.get("/calculate")
# async def calculate_profits():
    
#     order = "FIFO"                      # TODO: User input
#     fiat = "USD"                        # TODO: User input

#     files = get_files()
#     transactions = get_transactions_from_files(files)
#     amounts, transaction_profits, currency_transaction_profits, currency_profits = calculate_profit(transactions, order, fiat)

#     return {
#         "amounts": amounts,
#         "transaction_profits": transaction_profits,
#         "currency_transaction_profits": currency_transaction_profits,
#         "currency_profits": currency_profits
#     }

# @app.post("/files")
# async def create_upload_file(uploaded_file: UploadFile = File(...)):    
#     file_location = f"../files/{uploaded_file.filename}"
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(uploaded_file.file, file_object)    
#     return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

@app.get("/profits")
async def get_profits():
    cleaned_transaction_1 = ["2022-11-12", "USD", 1000, 1, "BTC", 1, 1000]
    cleaned_transaction_2 = ["2022-11-15", "BTC", 0.25, 1200, "USD", 300, 1]
    cleaned_transaction_3 = ["2022-11-18", "USD", 750, 1, "BTC", 0.5, 1500]
    cleaned_transaction_4 = ["2022-11-22", "USD", 500, 1, "ETH", 5, 100]
    cleaned_transaction_5 = ["2022-11-27", "USD", 200, 1, "LTC", 4, 50]
    cleaned_transaction_6 = ["2022-12-05", "ETH", 2.5, 80, "USD", 200, 1]
    cleaned_transactions = [
        cleaned_transaction_1,
        cleaned_transaction_2,
        cleaned_transaction_3,
        cleaned_transaction_4,
        cleaned_transaction_5,
        cleaned_transaction_6
    ]

    # Amounts
    amounts = {
        "per_day" : {"BTC": Stack(), "ETH": Stack(), "LTC": Stack(), "USD": Stack()},
        "total": {"BTC": 1.25, "ETH": 2.5, "LTC": 4, "USD": 0}    
    }
    amounts["per_day"]["BTC"].enqueue(["2022-11-15", 0.75])
    amounts["per_day"]["BTC"].enqueue(["2022-11-18", 0.5])
    amounts["per_day"]["ETH"].enqueue(["2022-11-22", 2.5])
    amounts["per_day"]["LTC"].enqueue(["2022-11-27", 4])
    amounts["per_day"]["USD"].enqueue(["2022-12-05", 0])           # TODO: Handle fiat amounts (can't be negative (-1950))

    # Profits
    transaction_profits = [0, 50, 0, 0, 0, -30]
    transaction_currency_profits = {"BTC": ["2022-11-15", 50], "ETH": ["2022-12-05", -30]}
    currency_profits = {"BTC": 50, "ETH": -30}          # LTC profit never realized. Not stored in currency_profits
    return {
        "transactions": cleaned_transactions,
        "amounts": amounts,
        "transaction_profits": transaction_profits,
        "transaction_currency_profits": transaction_currency_profits,
        "currency_profits": currency_profits
    }

@app.get("/prices")
async def get_prices():
    result_date = []
    result_data = []
    for i in range(0, 150):
        result_date.append(i)
        result_data.append(random.randint(1, 2)*i)

    return {
        "dates": result_date,
        "data": result_data
    }