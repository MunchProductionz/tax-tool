#Filer:
# / Overview
# Readers
# Datacleaner
# X Datastructures
# / Priceretriever
# X Calculation (Add features, fix TODOs)

from readers import get_files
from datacleaner import get_transactions_from_files


def run():

    files = get_files()
    transactions = get_transactions_from_files()

