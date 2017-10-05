from django.conf.urls import url

from pms.views.projects_views import ProjectView, IssueView, ProjectDetailsView, IssueDetailsView

urlpatterns = [
    url(r'^projects/$', ProjectView.as_view(), name="project-list-view"),
    url(r'^projects/(?P<slug>[\w-]+)/$', ProjectDetailsView.as_view(), name="project-details-view"),
    url(r'^issues/$', IssueView.as_view(), name="issue-list-view"),
    url(r'^issues/(?P<pk>[0-9]+)/$', IssueDetailsView.as_view(), name="issue-details-view"),
]
