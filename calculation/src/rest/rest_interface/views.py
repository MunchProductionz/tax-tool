## Sample code, should be deleted
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest.calculations.readers import get_files
from rest.calculations.datacleaner import get_transactions_from_files


class HealthView(APIView):
    """
    This viewset returns 200, if all is OK
    """

    def get(self, request, format=None):
        return Response("Ok", status=status.HTTP_200_OK)

class TransactionView(APIView):
    """
    This viewset returns the transactions of a given file
    """

    def get(self, request, format=None):
        files = get_files()
        transactions = get_transactions_from_files(files)
        return Response(transactions)