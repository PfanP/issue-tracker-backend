from rest_framework.generics import ListCreateAPIView

from pms.models.projects import Project, Issue
from pms.serializers.projects_serializers import ProjectSerializer, IssueSerializer

__author__ = 'Ashraful'


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter()


class IssueView(ListCreateAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.filter()
