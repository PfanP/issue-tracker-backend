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
    issue = models.ForeignKey('pms.Issue')
    action_by = models.ForeignKey('core.Profile', related_name='action_by')
    current_progress = models.IntegerField(default=0)
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
            issue = kwargs.get('issue')
            profile = kwargs.get('profile')
            progress = kwargs.get('progress')
            old_assignee = kwargs.get('old_assignee')
            new_assignee = kwargs.get('new_assignee')
            old_desc = kwargs.get('old_description')
            new_desc = kwargs.get('new_description')
            comment = kwargs.get('comment')
            # Creating instance now
            history = cls()
            history.issue_id = issue
            history.action_by_id = profile
            history.current_progress = progress
            history.old_assignee_id = old_assignee
            history.new_assignee_id = new_assignee
            history.old_description = old_desc
            history.new_description = new_desc
            history.comment = comment
            history.save()
            # Send an email to assigned user
            try:
                thread = threading.Thread(
                    target=cls.send_email(
                        email=history.new_assignee.user.email,
                        issue=history.issue_id,
                        user_name=history.new_assignee.name,
                        description=history.new_description
                    )
                )
                thread.start()
            except TypeError:
                # May be here can be an error log
                return history
            return history
        except Exception as err:
            # Here will be an error log
            pass

    @classmethod
    def send_email(cls, *args, **kwargs):
        email = kwargs.get('email')
        issue_number = kwargs.get('issue')
        user_name = kwargs.get('user_name')
        description = kwargs.get('description')
        if not email:
            return None
        message = mark_safe("""
            <h3 style="text-align: center">Issue #{0}</h3>
            <p><b>Assigned to:</b> {1}</p>
            <p><b>Description:</b> {2}</p>
            <p style="text-align: center"><b>This is automated email. please don't reply.</b></p>
        """.format(issue_number, user_name, description))
        status = send_mail(
            subject="Issue #{0}".format(issue_number),
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
            html_message=message
        )
        if status == 1:
            return True
        return False
