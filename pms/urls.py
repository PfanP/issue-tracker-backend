from django.conf.urls import url

from pms.views.projects_views import ProjectView, IssueView

urlpatterns = [
    url(r'^projects/$', ProjectView.as_view(), name="project-list-view"),
    url(r'^issues/$', IssueView.as_view(), name="issue-list-view"),
]
