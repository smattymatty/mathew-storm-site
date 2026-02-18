from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET

from .blog_feed import get_all_posts, get_featured_posts
# Import spellblocks to ensure they're registered
from . import spellblocks


def index(request):
    all_posts = get_all_posts()
    featured_posts = get_featured_posts(all_posts)

    context = {
        'page_title': 'Mathew Storm - Open Source Engineer & Writer',
        'meta_description': 'Open source engineer building sovereign infrastructure tools. Writing on technology, meaning, and the recursive absurd.',
        'meta_keywords': 'mathew storm, open source, django, philosophy, recursive absurd, digital sovereignty',
        'featured_posts': featured_posts[:2],
        'latest_posts': all_posts,
    }
    return render(request, 'A_base/home.html', context)

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

