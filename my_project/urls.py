from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

from core.views import landing

urlpatterns = [
    url('^$', landing.index),
    url(r'^api/v1/role-manager/', include('drf_role.urls')),
    url(r'^api/v1/core/', include('core.urls')),
    url(r'^api/v1/docs/', get_swagger_view(title='MyProject API')),
]
