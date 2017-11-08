from datetime import datetime

from rest_framework.generics import ListAPIView

from pms.models.issues import Issue


class ProgressReportChartView(ListAPIView):
    def get(self, request, *args, **kwargs):
        chart_data = {
            "line_chart": [],
            "pie_chart": [],
        }
        issues = Issue.objects.filter(
            created_at__gt=datetime.now()
        ).values('project__name', )
        return chart_data
