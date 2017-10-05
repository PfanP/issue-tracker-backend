from rest_framework import serializers

from core.serializers.profile_serializers import ProfileSerializer
from pms.helpers.enums import IssueStatusEnum, IssueTrackerEnum, IssuePriorityEnum
from pms.models.projects import Project, Issue
from pms.serializers.document_serializers import DocumentSerializer

__author__ = 'Ashraful'


class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'slug', 'name', 'description', 'website', 'documents')


class IssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    assigned_to = ProfileSerializer(read_only=True)
    watchers = ProfileSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = (
            'id', 'title', 'description', 'project', 'assigned_to', 'watchers', 'is_closed', 'progress', 'status',
            'tracker', 'priority', 'due_date'
        )

    def get_status(self, obj):
        return IssueStatusEnum(obj.status).name

    def get_tracker(self, obj):
        return IssueTrackerEnum(obj.tracker).name

    def get_priority(self, obj):
        return IssuePriorityEnum(obj.priority).name
