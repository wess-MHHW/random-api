from django.urls import include, path
from tasks import router


urlpatterns = [
    path(r"tasks/", include(router.router.urls))
]