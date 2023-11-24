from django.conf import settings
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# API URLS
urlpatterns = [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api-auth/", include("rest_framework.urls")),
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/",
         SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs", ),
    path("api/users/", include('users.urls', namespace='users')),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
