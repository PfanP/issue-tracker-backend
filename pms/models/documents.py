from django.db import models

from core.models.base import BaseEntity

__author__ = 'Ashraful'


class Document(BaseEntity):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/')

    class Meta:
        app_label = 'pms'
