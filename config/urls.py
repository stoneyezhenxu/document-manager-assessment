from django.conf import settings
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from propylon_document_manager.utils.global_value import GlobalValue

# API URLS
urlpatterns = [
    # API base url
    path(f"api/{GlobalValue.ApiVersion}/", include("config.api_router")),
    # DRF auth token
    path(f"{GlobalValue.ApiVersion}/api-auth/", include("rest_framework.urls")),
    path(f"{GlobalValue.ApiVersion}/auth-token/", obtain_auth_token),
    path(f"{GlobalValue.ApiVersion}/api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(f"api/{GlobalValue.ApiVersion}/docs/",
         SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs", ),
    path(f"api/{GlobalValue.ApiVersion}/users/", include('users.urls', namespace='users')),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
