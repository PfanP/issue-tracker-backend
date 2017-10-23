from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError

from core.models import Profile
from drf_role.models import Role

ROLE_NAMES = ('Admin', 'Manager', 'Developer', 'Tester',)
USER_NAMES = ('robin', 'ashraful', 'john', 'jasica')


class Command(BaseCommand):
    def handle(self, *args, **options):
        roles = Role.objects.all()
        for _index, role in enumerate(roles):
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=USER_NAMES[_index], password='1234')
                    Profile.objects.create(user_id=user.pk, role_id=role.pk)
            except IntegrityError:
                continue
        print("Users Created!!")
