from pathlib import Path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET

from django_spellbook.parsers import spellbook_render
# Import spellblocks to ensure they're registered
from . import spellblocks

content_folder = Path(__file__).resolve().parent / 'content'

def index(request):
    about_md = """---

## About

Open source engineer focused on federated systems, self-hosted infrastructure, and tools that put control back in users' hands. Creating Django-based solutions for organizations that value transparency, sovereignty, and the results.
"""

    connect_md = """
"""

    beliefs_md = """---

"""

    context = {
        # SEO metadata for homepage
        'page_title': 'Mathew Storm - Open Source Engineer',
        'meta_description': 'Founder building Storm Cloud Server, Django Spellbook, and Django Mercury. Open source engineer focused on federated infrastructure and digital sovereignty.',
        'meta_keywords': 'mathew storm, storm cloud server, django spellbook, federated infrastructure, digital sovereignty, activitypub, django developer',
        # Rendered markdown sections
        'about_section': spellbook_render(about_md),
        'connect_section': spellbook_render(connect_md),
        'beliefs_section': spellbook_render(beliefs_md),
    }
    template = 'A_base/home.html'
    return render(request, template, context)

@require_POST
def toggle_theme(request):
    """Toggle between light and dark mode."""
    current_mode = request.session.get('theme_mode', 'light')
    new_mode = 'dark' if current_mode == 'light' else 'light'

    request.session['theme_mode'] = new_mode
    request.session.save()

    # If HTMX request, return a small response to trigger page refresh
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Refresh'] = 'true'  # Tell HTMX to refresh the page
        return response

    # Otherwise redirect back
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_GET
def robots_txt(request):
    """Generate robots.txt file for search engines"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /a-panel/",
        "Disallow: /admin/",
        "Disallow: /static/",
        "",
        "Sitemap: https://mathewstorm.ca/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

