from django.urls import include, path
from house import router


urlpatterns = [
    path(r"house/", include(router.router.urls))
]