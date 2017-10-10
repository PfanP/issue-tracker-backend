from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView

from pms.models.projects import Project, Issue
from pms.serializers.issues_serializers import IssueSerializer
from pms.serializers.projects_serializers import ProjectSerializer

__author__ = 'Ashraful'


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter()


class ProjectDetailsView(RetrieveUpdateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter()
    lookup_field = 'slug'


class ProjectIssuesView(ListAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Issue.objects.filter(project__slug=slug)
        return queryset
