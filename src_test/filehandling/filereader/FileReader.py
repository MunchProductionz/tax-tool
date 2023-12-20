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