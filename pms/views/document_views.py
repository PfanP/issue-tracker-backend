from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FileUploadParser

from pms.models.documents import Document
from pms.serializers.document_serializers import DocumentSerializer

__author__ = 'Ashraful'


class DocumentView(ListCreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (FileUploadParser,)
    queryset = Document.objects.filter()
