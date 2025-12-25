from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from .sitemaps import SpellbookContentSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'content': SpellbookContentSitemap,
}

urlpatterns = [
    path('a-panel/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # Legacy /philo/ redirects to /writing/philosophy/
    path('philo/the-recursive-absurd/', RedirectView.as_view(
        url='/writing/philosophy/the-recursive-absurd/', permanent=True)),
    path('', include('A_base.urls')),
    path('questions/', include('questions.urls')),
    path('', include('django_spellbook.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
