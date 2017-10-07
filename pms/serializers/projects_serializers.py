from rest_framework import serializers

from core.serializers.profile_serializers import ProfileLiteSerializer
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
    assigned_to = ProfileLiteSerializer(read_only=True)
    watchers = ProfileLiteSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    due_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issue
        fields = (
            'id', 'title', 'description', 'project', 'author', 'assigned_to', 'watchers', 'is_closed', 
            'progress', 'status', 'tracker', 'priority', 'due_date', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'author'
        )

    def get_author(self, obj):
        return obj.author.name if obj.author else 'N/A'

    def get_due_date(self, obj):
        try:
            return obj.due_date.strftime("%d %b, %Y")
        except Exception:
            return 'N/A'

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %b, %Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d %b, %Y")
