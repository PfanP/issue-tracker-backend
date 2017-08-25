from django.conf.urls import url

from core.views.profile_views import ProfileView, LoginView, RegistrationView

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^registration/$', RegistrationView.as_view()),
    url(r'^profiles/$', ProfileView.as_view(), name="profile-list-view"),
]
