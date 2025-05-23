"""
URL configuration for cvproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView)

from main.views import (
    CVInstanceListView, CVInstanceDetailView,
    generate_cv_pdf, request_log_list,
    settings_view, send_cv_email_view, translate_cv,
)
from main.api_views import (
    CVInstanceAPIView, CVInstanceDetailedAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", CVInstanceListView.as_view(), name="cvinstance-list"),
    path(
        "cv/<int:pk>/",
        CVInstanceDetailView.as_view(),
        name="cvinstance-detail"
    ),
    path("cv/<int:pk>/download-pdf/", generate_cv_pdf, name="cv-pdf"),
    path(
        'api/cvs/',
        CVInstanceAPIView.as_view(),
        name='api-cvinstance-list',
    ),
    path(
        'api/cvs/<int:pk>/',
        CVInstanceDetailedAPIView.as_view(),
        name='api-cvinstance-detail',
    ),
    # Generate API schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI (interactive API documentation)
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    # Redoc UI (alternative API documentation)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path("requests/", request_log_list, name="request-log-list"),
    path("settings/", settings_view, name="settings"),
    path(
        "send-cv-email/<int:pk>/",
        send_cv_email_view,
        name="send-cv-email",
    ),
    path('cv/<int:pk>/translate/', translate_cv, name='translate-cv'),
]
