from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from fairplay_server.ksm.api.views import content_key_view
from fairplay_server.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

urlpatterns = [path("content-key", content_key_view)]


app_name = "api"
urlpatterns += router.urls
