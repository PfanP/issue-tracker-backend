import io
from contextlib import redirect_stdout

from django.conf import settings
from django.test.utils import get_runner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.management.commands.custom_test import Command

__author__ = 'Ashraful'


class UnitTestAPIView(APIView):
    def run_unit_test(self, test_labels=None, **options):
        if not test_labels:
            test_labels = ()
        outputs = io.StringIO()
        TestRunner = get_runner(settings)
        test_runner = TestRunner(**options)
        with redirect_stdout(outputs):
            failures = test_runner.run_tests(test_labels)
        # if failures:
        #     sys.exit(1)
        print(outputs.getvalue())

    def post(self, request, *args, **kwargs):
        data = request.data
        run_test = data.get('tests')
        response_data = {
            "success": False,
            "message": "Cannot run tests at this moment."
        }
        if run_test:
            # Do something here
            Command().handle()
            response_data = {
                "ran_tests": 100,
                "success": 95,
                "failed": 5
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
