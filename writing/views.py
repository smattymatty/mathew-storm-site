from pathlib import Path
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django_spellbook.parsers import render_spellbook_markdown_to_html
import re


# Path to writing content
WRITING_CONTENT_DIR = Path(__file__).resolve().parent.parent / 'writing_content'
CONTENT_DIR = WRITING_CONTENT_DIR / 'labyrinth-of-sisyphus'
METIS_CONTENT_DIR = WRITING_CONTENT_DIR / 'metis-wisdom-consumed'
SHORT_STORIES_DIR = WRITING_CONTENT_DIR / 'short-stories'


def estimate_line_count(text, chars_per_line=65):
    """
    Estimate how many visual lines a paragraph will take when rendered.

    Args:
        text: The paragraph text
        chars_per_line: Average characters per line (accounting for wrapping)

    Returns:
        Estimated number of lines this text will occupy
    """
    # Count explicit line breaks
    explicit_lines = text.count('\n') + 1

    # Estimate wrapped lines
    total_chars = len(text)
    wrapped_lines = (total_chars + chars_per_line - 1) // chars_per_line

    # Return the maximum (accounts for both explicit breaks and wrapping)
    return max(explicit_lines, wrapped_lines)


def paginate_chapter(markdown_content, max_lines_per_page=28, chars_per_line=65):
    """
    Intelligently split markdown content into book-like pages based on line count.

    Strategy:
    - Split on paragraph boundaries (double newlines)
    - Count estimated visual lines (including text wrapping)
    - Target max 28 lines per page for consistent reading experience
    - Never split mid-paragraph
    - Preserve markdown formatting

    Args:
        markdown_content: The raw markdown text
        max_lines_per_page: Maximum lines allowed per page
        chars_per_line: Average characters per line (for wrapping calculation)
    """
    # Split into paragraphs
    paragraphs = markdown_content.split('\n\n')

    pages = []
    current_page = []
    current_line_count = 0

    for para in paragraphs:
        # Skip empty paragraphs
        if not para.strip():
            continue

        # Estimate how many lines this paragraph will take
        para_lines = estimate_line_count(para, chars_per_line)

        # Add 1 line for the paragraph spacing
        para_lines_with_spacing = para_lines + 1

        # If adding this paragraph would exceed max lines, start new page
        if current_line_count > 0 and (current_line_count + para_lines_with_spacing > max_lines_per_page):
            # Save current page
            pages.append('\n\n'.join(current_page))
            # Start new page with this paragraph
            current_page = [para]
            current_line_count = para_lines_with_spacing
        else:
            # Add to current page
            current_page.append(para)
            current_line_count += para_lines_with_spacing

    # Add final page if any content remains
    if current_page:
        pages.append('\n\n'.join(current_page))

    return pages


def get_chapter_list(content_dir=None):
    """Get list of all chapters in order."""
    if content_dir is None:
        content_dir = CONTENT_DIR

    chapters = []

    # Debug: Check if content directory exists
    if not content_dir.exists():
        print(f"WARNING: Content directory does not exist: {content_dir}")
        return []

    # Get all chapter files (they're in the flat writing_content directory)
    all_chapter_files = sorted(content_dir.glob("Chapter *.md"))

    for file in all_chapter_files:
        # Extract chapter number from filename like "Chapter 1 - The Arrival.md"
        match = re.match(r"Chapter (\d+)", file.stem)
        if match:
            chapter_num = int(match.group(1))
            slug = file.stem.lower().replace(' ', '-')
            title = file.stem
            chapters.append({
                'number': chapter_num,
                'slug': slug,
                'title': title,
                'file': file
            })

    return sorted(chapters, key=lambda x: x['number'])


def index(request):
    """Writing dashboard with novels and short stories."""
    return render(request, 'writing/dashboard.html')


def book_cover(request):
    """Book cover / table of contents for The Labyrinth of Sisyphus."""
    chapters = get_chapter_list()

    context = {
        'chapters': chapters,
        'book_title': 'The Labyrinth of Sisyphus',
        'book_subtitle': 'A reimagining of Greek mythology through the lens of absurdism',
    }
    return render(request, 'writing/book_cover.html', context)


def metis_cover(request):
    """Book cover / table of contents for Metis: Wisdom Consumed."""
    chapters = get_chapter_list(METIS_CONTENT_DIR)

    context = {
        'chapters': chapters,
        'book_title': 'Metis: Wisdom Consumed',
        'book_subtitle': 'Before Zeus, there was wisdom',
    }
    return render(request, 'writing/metis_cover.html', context)


def read_chapter(request, book_slug, chapter_slug):
    """Main chapter reading view with pagination."""
    # Get page number from query params (default to 1)
    try:
        page_num = int(request.GET.get('page', 1))
    except (ValueError, TypeError):
        page_num = 1

    # Map book slug to content directory
    book_dirs = {
        'labyrinth-of-sisyphus': CONTENT_DIR,
        'metis-wisdom-consumed': METIS_CONTENT_DIR,
    }

    content_dir = book_dirs.get(book_slug)
    if not content_dir:
        raise Http404("Book not found")

    # Find the chapter file
    chapter_file = None
    chapter_info = None
    for chapter in get_chapter_list(content_dir):
        if chapter['slug'] == chapter_slug:
            chapter_file = chapter['file']
            chapter_info = chapter
            break

    if not chapter_file or not chapter_file.exists():
        raise Http404("Chapter not found")

    # Read the markdown content
    with open(chapter_file, 'r', encoding='utf-8') as f:
        raw_markdown = f.read()

    # Paginate the content
    pages = paginate_chapter(raw_markdown)
    total_pages = len(pages)

    # Validate page number (must be >= 1)
    if page_num < 1 or page_num > total_pages:
        page_num = 1

    # Get current page content
    current_page_markdown = pages[page_num - 1]
    current_page_html = render_spellbook_markdown_to_html(current_page_markdown)

    # Get all chapters for navigation (from the same book)
    all_chapters = get_chapter_list(content_dir)
    current_chapter_index = next((i for i, c in enumerate(all_chapters) if c['slug'] == chapter_slug), 0)

    prev_chapter = all_chapters[current_chapter_index - 1] if current_chapter_index > 0 else None
    next_chapter = all_chapters[current_chapter_index + 1] if current_chapter_index < len(all_chapters) - 1 else None

    # Calculate progress percentage
    progress_percent = int((page_num / total_pages) * 100) if total_pages > 0 else 0

    context = {
        'book_slug': book_slug,
        'chapter': chapter_info,
        'page_content': current_page_html,
        'current_page': page_num,
        'total_pages': total_pages,
        'progress_percent': progress_percent,
        'has_prev': page_num > 1,
        'has_next': page_num < total_pages,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'all_chapters': all_chapters,
    }

    return render(request, 'writing/read_chapter.html', context)


def get_page_htmx(request, book_slug, chapter_slug, page_num):
    """HTMX endpoint to return just the page content."""
    page_num = int(page_num)
    print(f"[DEBUG] HTMX request for book: {book_slug}, chapter: {chapter_slug}, page: {page_num}")

    # Map book slug to content directory
    book_dirs = {
        'labyrinth-of-sisyphus': CONTENT_DIR,
        'metis-wisdom-consumed': METIS_CONTENT_DIR,
    }

    content_dir = book_dirs.get(book_slug)
    if not content_dir:
        return render(request, 'writing/partials/page_not_found.html')

    # Find the chapter file
    chapter_file = None
    for chapter in get_chapter_list(content_dir):
        if chapter['slug'] == chapter_slug:
            chapter_file = chapter['file']
            break

    if not chapter_file or not chapter_file.exists():
        return render(request, 'writing/partials/page_not_found.html')

    # Read and paginate
    with open(chapter_file, 'r', encoding='utf-8') as f:
        raw_markdown = f.read()

    pages = paginate_chapter(raw_markdown)

    if page_num < 1 or page_num > len(pages):
        return render(request, 'writing/partials/page_not_found.html')

    # Render the specific page
    page_markdown = pages[page_num - 1]
    page_html = render_spellbook_markdown_to_html(page_markdown)

    context = {
        'page_content': page_html,
        'current_page': page_num,
        'total_pages': len(pages),
    }

    response = render(request, 'writing/partials/page_content.html', context)

    # Add custom headers for JavaScript to read
    response['X-Current-Page'] = str(page_num)
    response['X-Total-Pages'] = str(len(pages))

    print(f"[DEBUG] Returning page {page_num} of {len(pages)}")

    return response


def red_shoes(request):
    """Display the Red Shoes short story."""
    story_file = SHORT_STORIES_DIR / 'Red Shoes.md'

    if not story_file.exists():
        raise Http404("Short story not found")

    # Read the markdown content
    with open(story_file, 'r', encoding='utf-8') as f:
        raw_markdown = f.read()

    # Calculate word count
    word_count = len(raw_markdown.split())

    # Render to HTML
    story_html = render_spellbook_markdown_to_html(raw_markdown)

    context = {
        'story_title': 'Red Shoes',
        'story_subtitle': 'Black Mirror inspired story about a productivity app that works a little too well.',
        'story_content': story_html,
        'word_count': f"{word_count:,}",  # Format with commas
    }

    return render(request, 'writing/short_story.html', context)


def minimum_viable_apocalypse(request):
    """Display the Minimum Viable Apocalypse short story."""
    story_file = SHORT_STORIES_DIR / 'Minimum Viable Apocalypse.md'

    if not story_file.exists():
        raise Http404("Short story not found")

    # Read the markdown content
    with open(story_file, 'r', encoding='utf-8') as f:
        raw_markdown = f.read()

    # Calculate word count
    word_count = len(raw_markdown.split())

    # Render to HTML
    story_html = render_spellbook_markdown_to_html(raw_markdown)

    context = {
        'story_title': 'Minimum Viable Apocalypse',
        'story_subtitle': 'Corporate satire meets cosmic dread. The apocalypse needs better Q4 projections.',
        'story_content': story_html,
        'word_count': f"{word_count:,}",  # Format with commas
    }

    return render(request, 'writing/short_story.html', context)


def year_47_post_stitch(request):
    """Display the Year 47 Post Stitch short story."""
    story_file = SHORT_STORIES_DIR / 'Year 47 Post Stitch.md'

    if not story_file.exists():
        raise Http404("Short story not found")

    # Read the markdown content
    with open(story_file, 'r', encoding='utf-8') as f:
        raw_markdown = f.read()

    # Calculate word count
    word_count = len(raw_markdown.split())

    # Render to HTML
    story_html = render_spellbook_markdown_to_html(raw_markdown)

    context = {
        'story_title': 'Year 47 Post Stitch',
        'story_subtitle': 'A soil surgeon stitches bio-thread into a dying Earth while crystalline bioluminescent plants consume it faster than she can repair.',
        'story_content': story_html,
        'word_count': f"{word_count:,}",  # Format with commas
    }

    return render(request, 'writing/short_story.html', context)
