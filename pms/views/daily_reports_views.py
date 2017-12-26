from collections import OrderedDict
from datetime import datetime

from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from pms.models import Issue, Project


class DailyReportsView(APIView):
    def get(self, request, *args, **kwargs):
        data = dict()
        data['project_wise'] = self.get_project_wise_data()
        data['user_wise'] = self.get_user_wise_data()
        return Response(data=data)

    def get_user_wise_data(self):
        today = datetime.now()
        time_from = today.replace(hour=0, minute=0, second=0)
        time_to = today.replace(hour=23, minute=59, second=59)

        base_queryset = Issue.objects.filter(updated_at__gte=time_from, updated_at__lte=time_to)
        report_data = list()
        plain_data = base_queryset.values(
            'updated_by_id', 'updated_by__user__username', 'project__slug', 'project__name',
            today_updated=Count('pk'), total_progress=Sum('progress')
        )
        for d in plain_data:
            project = Project.objects.filter(slug=d.get('project__slug')).first()
            data = OrderedDict()
            data['updated_by_id'] = d.get('updated_by_id')
            data['updated_by_name'] = d.get('updated_by__user__username', 'System Bot')
            data['project_slug'] = d.get('project__slug')
            data['project_name'] = d.get('project__name')
            data['total_progress'] = int(d.get('total_progress') / project.issue_set.count())
            report_data.append(data)
        return report_data

    def get_project_wise_data(self):
        today = datetime.now()
        time_from = today.replace(hour=0, minute=0, second=0)
        time_to = today.replace(hour=23, minute=59, second=59)

        base_queryset = Issue.objects.filter(updated_at__gte=time_from, updated_at__lte=time_to)
        report_data = list()
        plain_data = base_queryset.values('project_id', 'project__name').annotate(today_updated=Count('pk'))
        for d in plain_data:
            data = OrderedDict()
            project = Project.objects.get(pk=d.get('project_id'))
            data['project'] = project.name
            data['total_issues'] = project.issue_set.count()
            data['today_updated'] = d.get('today_updated')
            data['today_created'] = project.issue_set.filter(created_at__gte=time_from, created_at__lte=time_to).count()
            report_data.append(data)
        return report_data
