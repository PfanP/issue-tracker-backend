from django.conf.urls import url, include

from core.views import landing

urlpatterns = [
    url('^$', landing.index),
    url(r'^api/v1/role-manager/', include('drf_role.urls')),
    url(r'^api/v1/core/', include('core.urls')),
]
