import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

__author__ = 'Ashraful'


class UnitTestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        run_test = data.get('tests')
        response_data = {
            "success": False,
            "message": "Cannot run tests at this moment."
        }
        if run_test:
            output = os.popen("python manage.py test").read()
            response_data = {
                "result": str(output)
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
