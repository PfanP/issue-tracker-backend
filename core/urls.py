from django.conf.urls import url

from core.views.profile_views import ProfileView, LoginView, RegistrationView, LogoutView
from core.views.tests_views import UnitTestAPIView
from core.views.user_settings_view import UserConfirmView

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^registration/$', RegistrationView.as_view()),
    url(r'^confirm-user/$', UserConfirmView.as_view()),
    url(r'^profiles/$', ProfileView.as_view(), name="profile-list-view"),
    url(r'^run-tests/$', UnitTestAPIView.as_view(), name="run-test-api"),
]
