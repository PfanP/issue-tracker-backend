from rest_framework import serializers

from core.serializers.profile_serializers import ProfileLiteSerializer
from pms.helpers.enums import ActionEnum
from pms.models.activity_log import ActivityLog
from pms.models.issues import Issue
from pms.models.projects import Project

__author__ = 'Ashraful'


class ActivityLogSerializer(serializers.ModelSerializer):
    profile = ProfileLiteSerializer(read_only=True)
    action = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ActivityLog
        fields = (
            'id', 'profile', 'action', 'operational_text', 'link', 'model_name', 'created_at', 'updated_at'
        )

    def get_link(self, obj):
        """
        This is STATIC url generator for each action.
        :param obj: object instance of ActivityLog
        :return: a path for make url from frontend
        """
        path = None
        if obj.model_name == Project.__name__:
            if obj.reference_id:
                p = Project.objects.filter(pk=obj.reference_id).first()
                path = "/projects/{0}".format(p.slug if p else "")
            else:
                path = "/projects"

        if obj.model_name == Issue.__name__:
            if obj.reference_id:
                issue_pk = obj.reference_id
                path = "/issues/{0}".format(issue_pk)
            else:
                path = "/issues"

        return path

    def get_action(self, obj):
        return ActionEnum(obj.action).name

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %b, %Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d %b, %Y")
