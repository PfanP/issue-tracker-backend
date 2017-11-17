from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from pms.models.documents import Document
from pms.serializers.document_serializers import DocumentSerializer

__author__ = 'Ashraful'


class DocumentListView(ListAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (FileUploadParser,)
    queryset = Document.objects.filter()


class DocumentCreateView(ListCreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = (FileUploadParser, )
    queryset = Document.objects.filter()

    # def perform_create(self, serializer):
    #     serializer.save()
    def post(self, request, *args, **kwargs):
        data = request.data
        if 'file' in data:
            data.pop('file')
        serialize = self.serializer_class(data=data)
        if serialize.is_valid(raise_exception=True):
            instance = serialize.save()
            f = request.FILES.get('file')
            instance.file = f
            instance.save()
            return Response(data=serialize.data)
        return Response(data=serialize.data)

