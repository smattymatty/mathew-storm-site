from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .sitemaps import SpellbookContentSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'content': SpellbookContentSitemap,
}

urlpatterns = [
    path('a-panel/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('A_base.urls')),
    path('', include('django_spellbook.urls')),
    path('questions/', include('questions.urls')),
    path('writing/', include('writing.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
