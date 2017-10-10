from rest_framework import serializers

from pms.models.projects import Project
from pms.serializers.document_serializers import DocumentSerializer

__author__ = 'Ashraful'


class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'slug', 'name', 'description', 'website', 'documents')


class ProjectLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'slug', 'name',)
