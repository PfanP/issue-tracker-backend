from rest_framework import serializers

from core.serializers.profile_serializers import ProfileLiteSerializer
from pms.helpers.enums import ActionEnum
from pms.models.activity_log import ActivityLog

__author__ = 'Ashraful'


class ActivityLogSerializer(serializers.ModelSerializer):
    profile = ProfileLiteSerializer(read_only=True)
    action = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = (
            # TODO: Here model_name will be change according to frontend need
            'id', 'profile', 'action', 'operational_text', 'model_name'
        )

    def get_action(self, obj):
        return ActionEnum(obj.action).name
