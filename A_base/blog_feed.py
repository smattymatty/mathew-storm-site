import yaml
from pathlib import Path
from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional

from django.conf import settings


@dataclass
class PostEntry:
    title: str
    path: str
    published: Optional[datetime]
    description: str
    tags: list
    category: str
    priority: float
    featured: bool


def _parse_date(value) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S'):
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                continue
    return None


def _url_from_md_path(md_file: Path, content_dir: Path, url_prefix: str) -> str:
    relative = md_file.relative_to(content_dir)
    url_path = str(relative).replace('.md', '').replace('\\', '/')
    # Strip leading dashes from each path component (Spellbook ordering convention)
    parts = url_path.split('/')
    parts = [p.lstrip('-') for p in parts]
    url_path = '/'.join(parts)
    return f'/{url_prefix}/{url_path}/'


EXCLUDED_STEMS = {'intro', 'philosophy_index', 'philosophy_glossary'}


def _should_exclude(md_file: Path, metadata: dict) -> bool:
    stem = md_file.stem.lstrip('-')
    if stem in EXCLUDED_STEMS:
        return True
    title = metadata.get('title', '').lower()
    if 'index' in title or 'glossary' in title:
        return True
    return False


def get_all_posts() -> list[PostEntry]:
    posts = []
    content_paths = settings.SPELLBOOK_MD_PATH
    url_prefixes = settings.SPELLBOOK_MD_URL_PREFIX

    for content_dir, url_prefix in zip(content_paths, url_prefixes):
        content_dir = Path(content_dir)
        if not content_dir.exists():
            continue

        for md_file in content_dir.glob('**/*.md'):
            try:
                raw = md_file.read_text(encoding='utf-8')
            except Exception:
                continue

            if not raw.startswith('---'):
                continue
            parts = raw.split('---', 2)
            if len(parts) < 3:
                continue
            try:
                metadata = yaml.safe_load(parts[1])
                if not isinstance(metadata, dict):
                    continue
            except yaml.YAMLError:
                continue

            if _should_exclude(md_file, metadata):
                continue

            title = metadata.get('title', md_file.stem.replace('-', ' ').title())

            published = None
            for key in ('published', 'created', 'date'):
                if key in metadata:
                    published = _parse_date(metadata[key])
                    if published:
                        break

            description = metadata.get('description', '')
            tags = metadata.get('tags', []) if isinstance(metadata.get('tags'), list) else []
            priority = float(metadata.get('sitemap_priority', 0.5))

            featured = bool(metadata.get('featured', False))

            posts.append(PostEntry(
                title=title,
                path=_url_from_md_path(md_file, content_dir, url_prefix),
                published=published,
                description=description,
                tags=tags,
                category=url_prefix,
                priority=priority,
                featured=featured,
            ))

    posts.sort(key=lambda p: p.published or datetime.min, reverse=True)
    return posts


def get_featured_posts(posts: list[PostEntry]) -> list[PostEntry]:
    return [p for p in posts if p.featured]
