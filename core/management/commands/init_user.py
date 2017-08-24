from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from core.models import Profile
from drf_role.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        roles = Role.objects.all()
        for role in roles:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=role.name.lower(), password='1234')
                    Profile.objects.create(user_id=user.pk, role_id=role.pk)
            except IntegrityError:
                continue
        print("Users Created!!")
