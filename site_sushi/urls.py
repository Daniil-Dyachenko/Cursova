from django.contrib import admin
from django.urls import path,include

from site_sushi import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('sushi.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
    path('basket/', include('baskets.urls', namespace='basket'))

]

if settings.DEBUG:
    urlpatterns += [ path("__debug__/", include("debug_toolbar.urls")), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)