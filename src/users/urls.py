from django.urls import path, include
from app import settings
from users import router

if settings.DEBUG:
    urls= [
        path("", include("rest_framework.urls")),
        path("", include("drf_social_oauth2.urls", namespace="drf")),
    ]

urlpatterns = [
    path(r"accounts/", include(router.router.urls)),
    path(r"auth/",include(urls))
]

