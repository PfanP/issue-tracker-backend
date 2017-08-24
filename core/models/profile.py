from django.contrib.auth.models import User
from django.db import models
from drf_role.models import Role

from core.helpers.enums import GenderEnum


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(verbose_name="Birth Date", null=True)
    gender = models.CharField(choices=GenderEnum.choices(), default=GenderEnum.MALE.value, max_length=16)
    mobile = models.CharField(max_length=16, unique=True, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
