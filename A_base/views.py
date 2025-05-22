from pathlib import Path

from django.shortcuts import render

from django_spellbook.parsers import render_spellbook_markdown_to_html

content_folder = Path(__file__).resolve().parent / 'content'

def index(request):
    with open(content_folder / 'home.md', 'r') as f:
        content = f.read()
    context = {
        'content': render_spellbook_markdown_to_html(content),
        'sidebar_header': 'This is my Home Page',
        }
    template = 'A_base/base.html'
    return render(request, template, context)

