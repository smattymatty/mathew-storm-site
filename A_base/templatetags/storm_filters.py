import json
import os
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ forloop.counter0|multiply:100 }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


# Cache for manifest data to avoid repeated file reads
_manifest_cache = {}


def _load_manifest(app_name):
    """Load and cache the spellbook manifest for an app."""
    if app_name in _manifest_cache:
        return _manifest_cache[app_name]

    manifest_path = os.path.join(settings.BASE_DIR, app_name, 'spellbook_manifest.json')
    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            # Build lookup dict: path -> title
            lookup = {}
            for page in data.get('pages', []):
                path = page.get('path', '').strip('/')
                title = page.get('title', '')
                if path and title:
                    lookup[path] = title
            _manifest_cache[app_name] = lookup
            return lookup
    except (FileNotFoundError, json.JSONDecodeError):
        _manifest_cache[app_name] = {}
        return {}


def _url_name_to_path(app_name, url_name):
    """
    Convert a url_name back to a path.
    url_name: philosophy_humanist-absurdism
    returns: writing/philosophy/humanist-absurdism
    """
    # Replace underscores with slashes to reconstruct path
    # This works because url_name is created by: clean_url.replace('/', '_')
    path_part = url_name.replace('_', '/')
    return f"{app_name}/{path_part}"


@register.filter
def page_title(namespaced_url):
    """
    Look up the page title from a namespaced URL.

    Usage: {{ prev_page|page_title }}
    Input: "writing:philosophy_humanist-absurdism"
    Output: "Humanist Absurdism: Choosing Humanity"
    """
    if not namespaced_url or ':' not in namespaced_url:
        return ''

    try:
        app_name, url_name = namespaced_url.split(':', 1)
        manifest = _load_manifest(app_name)

        # Convert url_name to path and look up
        path = _url_name_to_path(app_name, url_name)

        if path in manifest:
            return manifest[path]

        # Fallback: try to create a readable title from url_name
        # "philosophy_humanist-absurdism" -> "Humanist Absurdism"
        parts = url_name.split('_')
        if parts:
            last_part = parts[-1]  # Get the actual page name
            # Convert hyphens to spaces and title case
            return last_part.replace('-', ' ').title()

        return ''
    except Exception:
        return ''