from django.db import models
from core.models.base import BaseEntity
from pms.helpers.enums import ActionEnum


class ActivityLog(BaseEntity):
    user = models.ForeignKey('core.Profile')
    action = models.IntegerField(choices=ActionEnum.choices(), default=ActionEnum.RETRIEVE)
    operational_text = models.CharField(max_length=256, null=True, blank=True)
    model_name = models.CharField(max_length=64, null=True, blank=True)
    app_level = models.CharField(max_length=32, null=True, blank=True)
    reference_id = models.IntegerField()

    class Meta:
        app_level = 'pms'

    @classmethod
    def log(cls, *args, **kwargs):
        user = kwargs.get('user_id')
        action = kwargs.get('action', ActionEnum.RETRIEVE)
        operational_text = kwargs.get('op_text')
        model_name = kwargs.get('model_name')
        app_level = kwargs.get('app_level')
        reference_id = kwargs.get('reference_id')

        obj = cls()
        if not user:
            return obj, False