from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500,handler403
from api.views import iotRelayRequestView

urlpatterns = [
    path('', include('authentication.urls') ,name='home'),
    path('dashadmin/', include('dash_admin.urls')),
    path('dashtamu/', include('dash_tamu.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
handler404 = 'core.views.custom_page_not_found_view'
handler500 = 'core.views.custom_error_view'
handler403 = 'core.views.custom_permission_denied_view'
