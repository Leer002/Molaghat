from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("places.urls")),
    path('user/', include("users.urls")),
    path('', include("carts.urls")),
    path('', include("subscriptions.urls")),
    path('pay/', include("payments.urls")),
    path('', include("contacts.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
