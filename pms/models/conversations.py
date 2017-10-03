from django.db import models

from core.models.base import BaseEntity

__author__ = 'Ashraful'


class Reply(BaseEntity):
    text = models.CharField(max_length=360)

    class Meta:
        app_label = 'pms'


class Comment(BaseEntity):
    text = models.CharField(max_length=512)
    replies = models.ManyToManyField('pms.Reply')

    class Meta:
        app_label = 'pms'


class Conversation(BaseEntity):
    issue = models.ForeignKey('pms.Issue')
    comment = models.ForeignKey('pms.Comment')

    class Meta:
        app_label = 'pms'
