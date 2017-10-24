from django.conf.urls import url

from core.views.profile_views import ProfileView, LoginView, RegistrationView, LogoutView, ProfileDetailsView
from core.views.user_settings_view import UserConfirmView

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^registration/$', RegistrationView.as_view()),
    url(r'^confirm-user/$', UserConfirmView.as_view()),
    url(r'^profiles/$', ProfileView.as_view(), name="profile-list-view"),
    url(r'^profiles/(?P<pk>[0-9]+)/$', ProfileDetailsView.as_view(), name="profile-details-view"),
]
