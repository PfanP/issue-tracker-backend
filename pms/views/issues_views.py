from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from core.models.profile import Profile
from pms.helpers.enums import ActionEnum
from pms.models.activity_log import ActivityLog
from pms.models.conversations import Conversation
from pms.models.issues import Issue, IssueHistory
from pms.models.projects import Project
from pms.serializers.issues_serializers import IssueSerializer, IssueDetailsSerializer

__author__ = 'Ashraful'


class IssueView(ListCreateAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.filter()

    def get_queryset(self):
        queryset = self.queryset
        projects = self.request.GET.get('project', '').split(',')
        queryset = queryset.filter(project_id__in=projects)
        return queryset

    def post(self, request, *args, **kwargs):
        profile = request.user.profile.id
        serializer = self.serializer_class(data=request.data)
        response_data = {}
        if serializer.is_valid(raise_exception=True):
            project = request.data.get('project')
            assignee = request.data.get('assigned_to')
            try:
                project = Project.objects.get(pk=project).pk
            except (Project.DoesNotExist, AttributeError):
                response_data['project'] = ['No matching Project found.']
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            try:
                assignee = Profile.objects.get(pk=assignee).pk
            except (Profile.DoesNotExist, AttributeError):
                response_data['assigned_to'] = ['No matching User found.']
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            due_date = request.data.get('due_date')
            if due_date:
                due_date = datetime.strptime(due_date, "%Y-%m-%d") + timedelta(days=1)
            else:
                due_date = None
            watchers = request.data.get('watchers')
            instance = serializer.save(
                author_id=profile, project_id=project, assigned_to_id=assignee, due_date=due_date
            )
            if watchers:
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
    serializer_class = IssueDetailsSerializer
    queryset = Issue.objects.filter()

    def put(self, request, *args, **kwargs):
        profile = request.user.profile.id
        issue = self.get_object()
        # save some data to make a better history
        current_assignee = issue.assigned_to
        current_desc = issue.description
        old_progress = issue.progress
        serializer = IssueDetailsSerializer(issue, data=request.data)

        response_data = {}
        if serializer.is_valid(raise_exception=True):
            project = request.data.get('project')
            assignee = request.data.get('assigned_to')
            try:
                project = Project.objects.get(pk=project).pk
            except (Project.DoesNotExist, AttributeError):
                response_data['project'] = ['No matching Project found.']
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            try:
                assignee = Profile.objects.get(pk=assignee).pk
            except (Profile.DoesNotExist, AttributeError):
                response_data['assigned_to'] = ['No matching User found.']
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
            watchers = request.data.get('watchers')
            instance = serializer.save(
                author_id=profile, project_id=project, assigned_to_id=assignee,
            )
            if watchers:
                watchers_objects = list(Profile.objects.filter(pk__in=watchers))
                if instance:
                    # Save watchers to issues
                    instance.watchers.add(*watchers_objects)
            try:
                # Create activity log
                ActivityLog.log(
                    profile_id=request.user.profile.pk, action=ActionEnum.UPDATE.value,
                    op_text="{0} has updated [{1}]".format(request.user.profile.name, instance.title),
                    model_name=instance._meta.object_name, app_level=instance._meta.app_label,
                    reference_id=instance.pk
                )
                # Create History
                IssueHistory.create_history(
                    issue=instance.pk, profile=request.user.profile.pk,
                    new_progress=instance.progress, old_progress=old_progress,
                    old_assignee=current_assignee.pk, new_assignee=instance.assigned_to_id,
                    new_description=instance.description, old_description=current_desc,
                    comment="{0} has updated {1}".format(request.user.profile.name, instance.title)
                )
            except Exception:
                # Here can be a error log
                pass
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
