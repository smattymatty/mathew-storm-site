from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pathlib import Path
from django.conf import settings


class BaseSitemap(Sitemap):
    """Base sitemap with production URL handling"""
    protocol = 'https'  # Force HTTPS for production

    def get_urls(self, page=1, site=None, protocol=None):
        """Override to use production domain"""
        # Force the domain to be mathewstorm.ca in production
        if not settings.DEBUG:
            from django.contrib.sites.models import Site
            # Create a fake Site object with the correct domain
            class ProductionSite:
                domain = 'mathewstorm.ca'
                name = 'mathewstorm.ca'
            site = ProductionSite()

        return super().get_urls(page, site, protocol)


class SpellbookContentSitemap(BaseSitemap):
    """Sitemap for Django Spellbook markdown content"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """Get all markdown files and their URLs"""
        items = []

        # Iterate through each content directory
        for idx, content_path in enumerate(settings.SPELLBOOK_MD_PATH):
            url_prefix = settings.SPELLBOOK_MD_URL_PREFIX[idx]

            # Find all .md files
            for md_file in Path(content_path).glob('**/*.md'):
                relative_path = md_file.relative_to(content_path)
                url_path = str(relative_path).replace('.md', '').replace('\\', '/')

                # Build the full URL path
                if url_path == 'intro':
                    # intro files go to the root of the app
                    full_url = f'/{url_prefix}/'
                else:
                    # All other files keep their directory structure
                    full_url = f'/{url_prefix}/{url_path}/'

                items.append(full_url)

        return items

    def location(self, item):
        """Generate URL for each item - item is already the full path"""
        return item


class StaticViewSitemap(BaseSitemap):
    """Sitemap for static views"""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        """Return static view names"""
        return ['A_base:home', 'questions:questions_page']

    def location(self, item):
        """Generate URL for static views"""
        try:
            return reverse(item)
        except:
            return '/'