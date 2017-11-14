from datetime import datetime, timedelta

from django.db.models.aggregates import Sum, Count
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from pms.models.issues import Issue


class ProgressReportChartView(ListAPIView):
    @staticmethod
    def last_day_of_month(any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)

    def get(self, request, *args, **kwargs):
        chart_data = {
            "line_chart": {'data': [], "labels": []},
            "pie_chart": {},
        }
        now = datetime.now()
        project_wise_data = {}
        for month_num in range(1, 13):
            from_date = now.replace(month=month_num, day=1, minute=0, second=0)
            to_date = self.last_day_of_month(now.replace(month=month_num, minute=23, second=59))
            issues = Issue.objects.filter(
                created_at__gte=from_date, created_at__lt=to_date
            ).values('project__name', 'project_id').annotate(
                total_progress=Sum('progress'), issue_count=Count('pk')
            )
            pie_chart_data = {"labels": [], "data": []}
            for issue in issues:
                line_chart_data = {}
                if issue.get('project_id') in project_wise_data.keys():
                    project_wise_data[issue.get('project_id')].append(
                        issue.get('total_progress') // issue.get('issue_count'))
                else:
                    project_wise_data[issue.get('project_id')] = [
                        issue.get('total_progress') // issue.get('issue_count')]
                line_chart_data["label"] = issue.get('project__name')
                line_chart_data["pk"] = issue.get('project_id')
                if line_chart_data not in chart_data['line_chart']['data']:
                    chart_data['line_chart']['data'].append(line_chart_data)
                # Assign the pie chart data
                pie_chart_data["labels"].append(issue.get('project__name'))
                # push the labels to chart data
                this_month = now.replace(month=month_num).strftime("%B")
                if this_month not in chart_data["line_chart"]["labels"]:
                    chart_data["line_chart"]["labels"].append(this_month)
                pie_chart_data["data"].append(issue.get('total_progress') / issue.get('issue_count'))
            chart_data['pie_chart'] = pie_chart_data

        for chart, chart_data_list in chart_data.items():
            if chart == "line_chart":
                for data in chart_data_list['data']:
                    if data.get('pk') in project_wise_data.keys():
                        # used mutability concept
                        data["data"] = project_wise_data[data.get('pk')]

        return Response(data=chart_data, status=status.HTTP_200_OK)
