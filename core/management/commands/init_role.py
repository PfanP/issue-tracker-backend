from django.core.management.base import BaseCommand
from drf_role.models import Role
from psycopg2._psycopg import IntegrityError

ROLE_NAMES = ('Admin', 'Manager', 'Developer', 'Tester',)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _index, role_name in enumerate(ROLE_NAMES):
            try:
                Role.objects.get_or_create(name=role_name, type=_index)
            except IntegrityError:
                continue
        print("Created roles {0}".format(ROLE_NAMES))
