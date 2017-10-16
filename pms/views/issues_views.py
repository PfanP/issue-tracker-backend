from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from core.models.profile import Profile
from pms.helpers.enums import ActionEnum
from pms.models.activity_log import ActivityLog
from pms.models.conversations import Conversation
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
            due_date = request.data.get('due_date')
            if due_date:
                due_date = datetime.strptime(due_date, "%Y-%m-%d") + timedelta(days=1)
            watchers = request.data.get('watchers')
            instance = serializer.save(
                author_id=profile, project_id=project, assigned_to_id=assignee, due_date=due_date
            )
            watchers_objects = list(Profile.objects.filter(pk__in=watchers))
            if instance:
                # Save watchers to issues
                instance.watchers.add(*watchers_objects)
            try:
                # Create activity log
                ActivityLog.log(
                    profile_id=request.user.profile.pk, action=ActionEnum.CREATE.value,
                    op_text="{0} has created {1}".format(request.user.profile.name, instance.title),
                    model_name=instance._meta.object_name, app_level=instance._meta.app_label,
                    reference_id=instance.pk
                )
                # Create New conversation
                Conversation.objects.create(issue_id=instance.pk)
            except Exception:
                # Here can be a error log
                pass
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailsView(RetrieveUpdateAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.filter()
