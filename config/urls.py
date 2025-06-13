from django.conf import settings
from django.contrib import admin
from django.urls import path

from apps.user_auth.views import TestLoggingView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("ADMIN_URL", admin.site.urls),
    path("", TestLoggingView.as_view(), name="test"),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/schema/swagger/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(), name="redoc"),
]
admin.site.site_header = "NextGen Bank Admin"
admin.site.site_title = "NextGen Bank Admin Portal"
admin.site.index_title = "welcome to the NextGen Bank Admin Portal"
