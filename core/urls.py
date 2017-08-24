from django.conf.urls import url

from core.views.profile_views import ProfileView, LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="api-login"),
    url(r'^profiles/$', ProfileView.as_view(), name="profile-list-view"),
]
