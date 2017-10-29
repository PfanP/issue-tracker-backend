from autoslug import AutoSlugField
from django.db import models

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


class Issue(BaseEntity):
    title = models.CharField(max_length=256)
    description = models.TextField(verbose_name='Issue Description')
    author = models.ForeignKey('core.Profile', related_name='author')
    project = models.ForeignKey('pms.Project')
    assigned_to = models.ForeignKey('core.Profile', on_delete=models.SET_NULL, null=True, related_name='assigned_to')
    watchers = models.ManyToManyField('core.Profile', related_name='watchers')
    progress = models.IntegerField(default=0)
    status = models.IntegerField(choices=IssueStatusEnum.choices(), default=IssueStatusEnum.NEW.value)
    tracker = models.IntegerField(choices=IssueTrackerEnum.choices(), default=IssueTrackerEnum.BUG.value)
    priority = models.IntegerField(choices=IssuePriorityEnum.choices(), default=IssuePriorityEnum.LOW.value)
    due_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

    class Meta:
        app_label = 'pms'

    def __str__(self):
        return self.title[:32]


class IssueHistory(BaseEntity):
    action_by = models.ForeignKey('core.Profile', related_name='action_by')
    old_assignee = models.ForeignKey('core.Profile', related_name='old_assignee', null=True)
    new_assignee = models.ForeignKey('core.Profile', related_name='new_assignee', null=True)
    old_description = models.TextField(verbose_name='Old Description', null=True, blank=True)
    new_description = models.TextField(verbose_name='New Description', null=True, blank=True)
    comment = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        app_label = "pms"

    @classmethod
    def create_history(cls, *args, **kwargs):
        try:
            profile = kwargs.get('profile')
            old_assignee = kwargs.get('old_assignee')
            new_assignee = kwargs.get('new_assignee')
            old_desc = kwargs.get('old_description')
            new_desc = kwargs.get('new_description')
            comment = kwargs.get('comment')
            # Creating instance now
            history = cls()
            history.action_by_id = profile
            history.old_assignee_id = old_assignee
            history.new_assignee_id = new_assignee
            history.old_description = old_desc
            history.new_description = new_desc
            history.comment = comment
            history.save()
        except Exception as err:
            # Here will be an error log
            pass
