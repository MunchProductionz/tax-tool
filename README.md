# Tax-tool

## How to use
- Choose and upload a transaction log directly from a valid crypto exchange
- Choose wanted order (FIFO/LIFO)
- Choose wanted output fiat currency
- Press "Calculate Tax"
- Download Excel-file or view data on the page

## Results
There are three pages to the output Excel-file:
- Transactions: Ordered list of all transactions and their realized profit
- Results: Total profit on all currencies
- Assets: Overview of total assets, as well as an ordered list of changes to each asset

## Internal machinery
1. Files are read and output in a defined list-format using exchange-specific readers in readers.py
2. Filedata is combined and ordered in datacleaner.py
3. Calculations are made using the filedata, historic prices and the chosen order for calculation (FIFO/LIFO)
4. Output from calculations are written to an Excel-file and vizualized on the webpage

## Libraries Used
- Find filepaths: [Glob](https://docs.python.org/3/library/glob.html)
- Read files: Pandas [CSV](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) [Excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- Define Queue/Stack: [Deque](https://docs.python.org/3/library/collections.html#collections.deque)
- Get historic prices: (*FILL IN*)
- Write to excel: [XLSXwriter](https://xlsxwriter.readthedocs.io/)


## Websites Scraped
- CoinGecko: [Crypto](https://www.coingecko.com/en/coins/bitcoin/historical_data?start_date=20230215&end_date=20230216#panel)
- X-Rates: [Fiat](https://www.x-rates.com/historical/?from=USD&amount=1&date=2023-02-15)