from django.core.management.base import BaseCommand
from drf_role.models import Role

ROLE_NAMES = ('Admin', 'Manager', 'Developer', 'Tester',)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _index, role_name in enumerate(ROLE_NAMES):
            Role.objects.get_or_create(name=role_name, type=_index)
        print("Created roles {0}".format(ROLE_NAMES))
