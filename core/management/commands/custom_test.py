import io
import sys
from contextlib import redirect_stdout

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Discover and run tests in the specified modules or the current directory.'

    def handle(self, *test_labels, **options):
        from django.conf import settings
        from django.test.utils import get_runner
        outputs = io.StringIO()
        TestRunner = get_runner(settings)

        test_runner = TestRunner(**options)
        failures = 0
        with redirect_stdout(outputs):
            failures = test_runner.run_tests(test_labels)
        print("Printing Output...")
        print(outputs)

        if failures:
            sys.exit(1)
