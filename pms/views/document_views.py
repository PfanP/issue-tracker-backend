from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser

from pms.models.documents import Document
from pms.serializers.document_serializers import DocumentSerializer

__author__ = 'Ashraful'


class DocumentListView(ListAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (FileUploadParser,)
    queryset = Document.objects.filter()


class DocumentCreateView(ListCreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (FileUploadParser,)
    queryset = Document.objects.filter()

    def perform_create(self, serializer):
        serializer.save()

