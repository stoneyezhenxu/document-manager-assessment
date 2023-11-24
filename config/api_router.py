from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter, SimpleRouter
from propylon_document_manager.users.api.views import UserViewSet, LoginView, LogoutView, RegisterView
from propylon_document_manager.file_versions.api.views import FileVersionViewSet



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
router.register("users", UserViewSet)
router.register("files", FileVersionViewSet)
app_name = "api"
urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('register/', RegisterView.as_view(), name='api-register'),
]
urlpatterns += router.urls
