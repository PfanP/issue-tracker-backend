from collections import OrderedDict
from datetime import datetime

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from pms.models import Issue, Project


class DailyReportsView(APIView):
    def get(self, request, *args, **kwargs):
        data = dict()
        data['project_wise'] = self.get_project_wise_data()
        data['user_wise'] = self.get_user_wise_data()
        return Response(data=data)

    def get_project_wise_data(self):
        today = datetime.now()
        time_from = today.replace(hour=0, minute=0, second=0)
        time_to = today.replace(hour=23, minute=59, second=59)

        base_queryset = Issue.objects.filter(updated_at__gte=time_from, updated_at__lte=time_to)
        report_data = list()
        plain_data = base_queryset.values('project_id', 'project__name', today_updated=Count('pk'))
        for d in plain_data:
            data = OrderedDict()
            project = Project.objects.get(pk=d.get('project_id'))
            data['project'] = project.name
            data['total_issues'] = project.issue_set.count()
            data['today_updated'] = d.get('today_updated')
            data['today_created'] = project.issue_set.filter(created_at__gte=time_from, created_at__lte=time_to).count()
            report_data.append(data)
        return report_data

    def get_user_wise_data(self):
        today = datetime.now()
        time_from = today.replace(hour=0, minute=0, second=0)
        time_to = today.replace(hour=23, minute=59, second=59)

        base_queryset = Issue.objects.filter(updated_at__gte=time_from, updated_at__lte=time_to)
        report_data = list()
        plain_data = base_queryset.values('project_id', 'project__name', today_updated=Count('pk'))
        for d in plain_data:
            data = OrderedDict()
            project = Project.objects.get(pk=d.get('project_id'))
            data['project'] = project.name
            data['total_issues'] = project.issue_set.count()
            data['today_updated'] = d.get('today_updated')
            data['today_created'] = project.issue_set.filter(created_at__gte=time_from, created_at__lte=time_to).count()
            report_data.append(data)
        return report_data
