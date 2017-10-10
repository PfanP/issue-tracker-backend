from django.conf.urls import url

from pms.views.document_views import DocumentView
from pms.views.issues_views import IssueDetailsView, IssueView
from pms.views.projects_views import ProjectView, ProjectDetailsView

urlpatterns = [
    url(r'^documents/$', DocumentView.as_view(), name="document-list-view"),
    url(r'^projects/$', ProjectView.as_view(), name="project-list-view"),
    url(r'^projects/(?P<slug>[\w-]+)/$', ProjectDetailsView.as_view(), name="project-details-view"),
    url(r'^issues/$', IssueView.as_view(), name="issue-list-view"),
    url(r'^issues/(?P<pk>[0-9]+)/$', IssueDetailsView.as_view(), name="issue-details-view"),
]
