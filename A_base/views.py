from pathlib import Path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from django_spellbook.parsers import render_spellbook_markdown_to_html
# Import spellblocks to ensure they're registered
from . import spellblocks

content_folder = Path(__file__).resolve().parent / 'content'

def index(request):
    with open(content_folder / 'home.md', 'r') as f:
        content = f.read()
    context = {
        'content': render_spellbook_markdown_to_html(content),
        'sidebar_header': 'Welcome to my Digital Workshop',
        'hero': {
            'title': 'Mathew Storm',
            'subtitle': 'Full-Stack Developer & Open Source Enthusiast',
            'description': 'Building elegant solutions with Django, Python, and modern web technologies',
        }
    }
    template = 'A_base/base.html'
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

