from django.core.management.base import BaseCommand
from django.db import transaction

from drf_role.enums import RoleEnum, PermissionEnum
from drf_role.models import Role, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Creating permissions
        for enum in PermissionEnum:
            with transaction.atomic():
                Permission.objects.get_or_create(access_type=enum.value, access_type_name=enum.name)

        print("Permissions Loaded.")

        # Creating role
        for enum in RoleEnum:
            with transaction.atomic():
                Role.objects.get_or_create(name=enum.name, type=enum.value)

        print("Role Created.")
