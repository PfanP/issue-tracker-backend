from rest_framework.generics import ListAPIView

from pms.models.activity_log import ActivityLog
from pms.serializers.activity_logs_serializers import ActivityLogSerializer

__author__ = 'Ashraful'


class ActivityLogView(ListAPIView):
    serializer_class = ActivityLogSerializer
    queryset = ActivityLog.objects.filter()