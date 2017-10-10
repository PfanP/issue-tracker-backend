from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from pms.models.projects import Issue
from pms.serializers.issues_serializers import IssueSerializer

__author__ = 'Ashraful'


class IssueView(ListCreateAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.filter()

    def post(self, request, *args, **kwargs):
        profile = request.user.profile.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = request.data.get('project')
            assignee = request.data.get('assigned_to')
            serializer.save(author_id=profile, project_id=project, assigned_to_id=assignee)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailsView(RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.filter()
