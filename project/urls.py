from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/swagger/')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
