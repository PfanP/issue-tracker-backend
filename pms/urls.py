from django.conf.urls import url

from pms.views.activity_log_views import ActivityLogView
from pms.views.conversations_views import IssueConversationView, ConversationView, CommentView, ConversationDetailsView
from pms.views.document_views import DocumentCreateView, DocumentListView
from pms.views.issues_views import IssueDetailsView, IssueView
from pms.views.progress_report_chart_views import ProgressReportChartView
from pms.views.projects_views import ProjectView, ProjectDetailsView, ProjectIssuesView

urlpatterns = [
    url(r'^documents/$', DocumentListView.as_view(), name="document-list-view"),
    url(r'^documents/(?P<filename>[^/]+)$', DocumentCreateView.as_view(), name="document-list-view"),
    url(r'^projects/$', ProjectView.as_view(), name="project-list-view"),
    url(r'^projects/(?P<slug>[\w-]+)/$', ProjectDetailsView.as_view(), name="project-details-view"),
    url(r'^projects/(?P<slug>[\w-]+)/issues/$', ProjectIssuesView.as_view(), name="project-issues-list-view"),
    url(r'^issues/$', IssueView.as_view(), name="issue-list-view"),
    url(r'^issues/(?P<pk>[0-9]+)/$', IssueDetailsView.as_view(), name="issue-details-view"),
    url(r'^issues/(?P<pk>[0-9]+)/conversations/$', IssueConversationView.as_view(), name="issue-conversation-list-view"),
    url(r'^activity-logs/$', ActivityLogView.as_view(), name='activity-log-list-view'),
    url(r'^conversations/$', ConversationView.as_view(), name='conversations-list-view'),
    url(r'^conversations/(?P<pk>[0-9]+)/$', ConversationDetailsView.as_view(), name='conversations-details-view'),
    url(r'^conversations/(?P<pk>[0-9]+)/comments/$', CommentView.as_view(), name='comment-list-view'),
    url(r'^progress-report/$', ProgressReportChartView.as_view(), name="progress-report-view"),
]
