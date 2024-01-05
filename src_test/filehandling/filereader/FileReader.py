import glob
import pandas as pd
from typing import List
from ExchangeReaders import ExchangeReaders

class FileReader:
    
    def __init__(self):
        self.exchange_readers = ExchangeReaders()
        self.exchanges = self.exchange_readers.get_exchanges()
    
    # Get uploaded files
    def get_files(self) -> List[List[str, str]]:

        # TODO: Create method for storing files
        # TODO: Separate between different exchanges
        # TODO: Handle case when file is not valid type

        # Create lists of uploaded files
        files = list()          # TODO: Rewrite to use dictionary with lists instead of 2D-list
        
        # Get valid exchanges
        exchanges = self.exchanges

        # Add uploaded files' file_path and their exchanges to files
        for exchange in exchanges:
            for file_path in glob.glob("../files/*" + exchange + "*"):
                files.append([exchange, file_path])

        return files