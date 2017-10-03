from django.db import models
from autoslug import AutoSlugField

from core.models.base import BaseEntity
from pms.helpers.enums import IssueTrackerEnum, IssueStatusEnum, IssuePriorityEnum
from pms.models.documents import Document

__author__ = 'Ashraful'


class Project(BaseEntity):
    name = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True)
    documents = models.ManyToManyField(Document)

    class Meta:
        app_label = 'pms'


class Issue(BaseEntity):
    title = models.CharField(max_length=256)
    description = models.TextField(verbose_name='Issue Description')
    project = models.ForeignKey('pms.Project')
    assigned_to = models.ForeignKey('core.Profile', on_delete=models.SET_NULL, null=True, related_name='assigned_to')
    watchers = models.ManyToManyField('core.Profile', related_name='watchers')
    is_closed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    status = models.IntegerField(choices=IssueStatusEnum.choices(), default=IssueStatusEnum.NEW.value)
    tracker = models.IntegerField(choices=IssueTrackerEnum.choices(), default=IssueTrackerEnum.BUG.value)
    priority = models.IntegerField(choices=IssuePriorityEnum.choices(), default=IssuePriorityEnum.LOW.value)
    due_date = models.DateField(null=True)

    class Meta:
        app_label = 'pms'
