import threading

from autoslug import AutoSlugField
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils.safestring import mark_safe

from core.models.base import BaseEntity
from pms.helpers.enums import IssueTrackerEnum, IssueStatusEnum, IssuePriorityEnum
from pms.models.documents import Document

__author__ = 'Ashraful'


class Project(BaseEntity):
    name = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True)
    documents = models.ManyToManyField(Document)

    class Meta:
        app_label = 'pms'

    def __str__(self):
        return self.name[:32]
