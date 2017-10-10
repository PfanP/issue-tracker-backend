from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from pms.models.projects import Project
from pms.serializers.projects_serializers import ProjectSerializer

__author__ = 'Ashraful'


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter()


class ProjectDetailsView(RetrieveUpdateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter()
    lookup_field = 'slug'
