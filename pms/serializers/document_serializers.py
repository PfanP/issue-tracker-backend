from rest_framework import serializers

from pms.models.documents import Document

__author__ = 'Ashraful'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('title', 'description', 'file',)
