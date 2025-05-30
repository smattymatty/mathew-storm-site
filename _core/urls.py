from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('A_base.urls')),
    path('', include('django_spellbook.urls')),
    path('questions/', include('questions.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
