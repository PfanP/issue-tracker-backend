from django.db import models

from core.models.base import BaseEntity
from pms.helpers.enums import ActionEnum


class ActivityLog(BaseEntity):
    profile = models.ForeignKey('core.Profile')
    action = models.IntegerField(choices=ActionEnum.choices(), default=ActionEnum.RETRIEVE.value)
    operational_text = models.CharField(max_length=256, null=True, blank=True)
    model_name = models.CharField(max_length=64, null=True, blank=True)
    app_level = models.CharField(max_length=32, null=True, blank=True)
    reference_id = models.IntegerField(null=True)

    class Meta:
        app_label = 'pms'

    @classmethod
    def log(cls, *args, **kwargs):
        """
        Create or return instance with a boolean type success variable
        :param args:
        :param kwargs: all the value will come through kwargs
        :return: instance and success(True/False)
        """
        profile = kwargs.get('profile_id')
        action = kwargs.get('action', ActionEnum.RETRIEVE.value)
        operational_text = kwargs.get('op_text')
        model_name = kwargs.get('model_name')
        app_level = kwargs.get('app_level')
        reference_id = kwargs.get('reference_id')

        obj = cls()
        success = False
        if not profile:
            return obj, success
        try:
            obj.profile_id = profile
            obj.action = action
            obj.operational_text = operational_text
            obj.model_name = model_name
            obj.app_level = app_level
            obj.reference_id = reference_id
            obj.save()
            # set success
            success = True
        except Exception:
            pass
        return obj, success
