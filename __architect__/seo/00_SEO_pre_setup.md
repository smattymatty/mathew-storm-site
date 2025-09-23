# SEO Pre-Setup Strategy for mathewstorm.ca

## Executive Summary
Transform mathewstorm.ca into the authoritative source for **Mathew Storm**, **recursive absurdism**, and **AI-assisted engineering**. This document outlines a comprehensive SEO strategy leveraging Django Spellbook's unique capabilities to dominate search results for your name and philosophical concepts.

### Django Spellbook Integration
This strategy is optimized for Django Spellbook, which means:
- ✅ SEO metadata embedded directly in markdown files via SpellBlocks
- ✅ Automatic URL structure and navigation generation
- ✅ No need for manual meta tag management
- ✅ Content and SEO unified in one workflow

## Current Status Analysis

### Strengths
- Unique, brandable content (recursive absurd, techno-absurdism)
- Django-based architecture (SEO-friendly framework)
- Strong technical foundation with Django Spellbook
- Original philosophical and technical writing
- Clear site structure with distinct content pillars

### Opportunities
- No sitemap.xml implementation
- Missing structured data for author/personal brand
- Meta descriptions could be more targeted
- No robots.txt file configured
- Internal linking between philosophical concepts underutilized

## Phase 1: Technical SEO Foundation (Week 1)

### 1.1 Django Sitemap Implementation for Spellbook

Since Django Spellbook generates views from markdown (not models), we need a different approach:

```python
# _core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pathlib import Path
from django.conf import settings

class SpellbookContentSitemap(Sitemap):
    """Sitemap for Django Spellbook markdown content"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """Get all markdown files and their URLs"""
        items = []

        # Iterate through each content directory
        for idx, content_path in enumerate(settings.SPELLBOOK_MD_PATH):
            prefix = settings.SPELLBOOK_MD_URL_PREFIX[idx]
            app_name = settings.SPELLBOOK_MD_APP[idx]

            # Find all .md files
            for md_file in Path(content_path).glob('**/*.md'):
                relative_path = md_file.relative_to(content_path)
                url_path = str(relative_path).replace('.md', '').replace('\\', '/')

                # Skip intro files (they're at the root)
                if url_path == 'intro':
                    url_path = ''

                items.append(f"{app_name}:{url_path}" if url_path else f"{app_name}:intro")

        return items

    def location(self, item):
        """Generate URL for each item"""
        try:
            return reverse(item)
        except:
            # Fallback for items that don't resolve
            return '/'

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['A_base:home', 'questions:questions_page']  # Your static views

    def location(self, item):
        return reverse(item)

# _core/urls.py additions
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, SpellbookContentSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'content': SpellbookContentSitemap,
}

urlpatterns = [
    # ... existing patterns
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
```

### 1.2 Robots.txt Configuration

```python
# A_base/views.py
from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def robots_txt(request):
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

# A_base/urls.py
path('robots.txt', views.robots_txt),
```

### 1.3 Structured Data Implementation

```html
<!-- Add to base.html head section -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Mathew Storm",
  "url": "https://mathewstorm.ca",
  "image": "https://mathewstorm.ca/static/images/mathew-storm.jpg",
  "sameAs": [
    "https://github.com/smattymatty",
    "https://linkedin.com/in/mathew-storm-70b671384",
    "https://techhub.social/@smattymatty"
  ],
  "jobTitle": "CEO of Storm Development",
  "worksFor": {
    "@type": "Organization",
    "name": "Storm Development"
  },
  "description": "Leader of the 80-20 Human-In-The-Loop movement, philosophical author exploring humanity in the age of AI",
  "knowsAbout": ["AI-Assisted Engineering", "Recursive Absurdism", "Django Development", "Philosophy of Technology"],
  "alumniOf": {
    "@type": "CollegeOrUniversity",
    "name": "Your University"
  }
}
</script>

<!-- Article structured data for blog posts -->
{% if article %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ article.title }}",
  "author": {
    "@type": "Person",
    "name": "Mathew Storm"
  },
  "datePublished": "{{ article.created|date:'c' }}",
  "dateModified": "{{ article.updated|date:'c' }}",
  "description": "{{ article.description|truncatewords:30 }}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ request.build_absolute_uri }}"
  }
}
</script>
{% endif %}
```

## Phase 2: SEO SpellBlocks Implementation (Week 2)

### 2.1 Create Custom SEO SpellBlocks

Django Spellbook's SpellBlock system is perfect for embedding SEO metadata directly in markdown content.

```python
# A_base/spellblocks.py
from django_spellbook.blocks import BasicSpellBlock, SpellBlockRegistry

@SpellBlockRegistry.register()
class SEOBlock(BasicSpellBlock):
    """Embed SEO metadata directly in markdown files"""
    name = 'seo'
    template = 'A_base/blocks/seo_metadata.html'

    def get_context(self):
        context = super().get_context()
        context['title'] = self.kwargs.get('title', '')
        context['description'] = self.kwargs.get('description', '')
        context['keywords'] = self.kwargs.get('keywords', '')
        context['author'] = self.kwargs.get('author', 'Mathew Storm')
        context['og_image'] = self.kwargs.get('image', '')
        return context

@SpellBlockRegistry.register()
class MetaBlock(BasicSpellBlock):
    """Quick meta description block"""
    name = 'meta'
    template = 'A_base/blocks/meta_description.html'

    def get_context(self):
        context = super().get_context()
        context['description'] = self.kwargs.get('description', self.content[:155])
        return context

@SpellBlockRegistry.register()
class SchemaBlock(BasicSpellBlock):
    """Structured data for articles"""
    name = 'schema'
    template = 'A_base/blocks/schema_article.html'

    def get_context(self):
        context = super().get_context()
        context['type'] = self.kwargs.get('type', 'Article')
        context['headline'] = self.kwargs.get('headline', '')
        context['date'] = self.kwargs.get('date', '')
        return context
```

### 2.2 Create SpellBlock Templates

```html
<!-- A_base/templates/A_base/blocks/seo_metadata.html -->
{% if title %}
<meta property="og:title" content="{{ title }}">
<meta name="twitter:title" content="{{ title }}">
{% endif %}
{% if description %}
<meta name="description" content="{{ description|truncatechars:155 }}">
<meta property="og:description" content="{{ description|truncatechars:155 }}">
{% endif %}
{% if keywords %}
<meta name="keywords" content="{{ keywords }}">
{% endif %}

<!-- A_base/templates/A_base/blocks/meta_description.html -->
<meta name="description" content="{{ description|truncatechars:155 }}">

<!-- A_base/templates/A_base/blocks/schema_article.html -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "{{ type }}",
  "headline": "{{ headline }}",
  "author": {
    "@type": "Person",
    "name": "{{ author|default:'Mathew Storm' }}"
  },
  "datePublished": "{{ date }}",
  "publisher": {
    "@type": "Person",
    "name": "Mathew Storm"
  }
}
</script>
```

### 2.3 Usage in Markdown Content

Now you can embed SEO directly in your markdown files:

```markdown
{~ seo
   title="The Recursive Absurd: A Digital Addendum to Sisyphus"
   description="Exploring how we create systems that create us, leading to new forms of existential loops in the digital age"
   keywords="recursive absurd, Mathew Storm, digital philosophy, techno-absurdism"
~}

# The Recursive Absurd

{~ meta description="We no longer discover absurdity; we manufacture it. Where Camus confronted cosmic indifference, we face algorithmic indifference we designed ourselves." ~}

Your content here...
```

### 2.4 Quick Implementation Example

Update your existing `philo_content/the-recursive-absurd.md`:

```markdown
{~ seo
   title="The Recursive Absurd - Mathew Storm's Philosophy"
   description="Discover recursive absurdism: where we build systems that build us. A new philosophical framework by Mathew Storm extending Camus into the digital age."
   keywords="recursive absurd, recursive absurdism, Mathew Storm, digital philosophy, techno-absurdism, existentialism, Camus"
~}

{~ schema
   type="Article"
   headline="The Recursive Absurd: A Digital Addendum to Sisyphus"
   date="2025-01-01"
~}

# The Recursive Absurd: A Digital Addendum to Sisyphus

[Your existing content...]
```

## Phase 3: Content SEO Strategy (Weeks 3-4)

### 3.1 Target Keyword Matrix

| Primary Keywords | Search Volume | Competition | Current Rank | Target |
|-----------------|--------------|-------------|--------------|--------|
| Mathew Storm | Low | Low | Not ranking | #1 |
| Recursive absurd | Very Low | None | Not ranking | #1 |
| Recursive absurdism | Very Low | None | Not ranking | #1 |
| AI assisted engineering | Medium | Medium | Not ranking | Top 10 |
| Techno-absurdism | Very Low | Low | Not ranking | #1 |
| Humanist absurdism | Low | Low | Not ranking | #1 |
| Neo-absurdism | Very Low | None | Not ranking | #1 |
| Tech philosophy | Medium | High | Not ranking | Top 20 |
| 80-20 Human-in-the-Loop | Very Low | None | Not ranking | #1 |
| Django Spellbook | Low | Low | Not ranking | Top 3 |

### 3.2 Content Structure with Django Spellbook

Your URL structure based on `SPELLBOOK_MD_URL_PREFIX`:
- `/proj/` - Projects content
- `/tuts/` - Tutorials content
- `/blog/` - Blog posts
- `/note/` - Notes content
- `/philo/` - Philosophy content
- `/about/` - About pages (once created)

Example URLs generated:
- `https://mathewstorm.ca/philo/the-recursive-absurd`
- `https://mathewstorm.ca/blog/Artificial_Intelligence/vibe-Coding-vs-AI-Assisted-Engineering`
- `https://mathewstorm.ca/about/mathew-storm`

### 3.3 Content Optimization Checklist

For each markdown file:
- [ ] Add SEO SpellBlock at the top with title, description, keywords
- [ ] Use `{~ seo ~}` block with 155-char description including primary keyword
- [ ] H1 tag (# heading) contains keyword variation
- [ ] First 100 words mention primary keyword
- [ ] 2-3 H2 subheadings with LSI keywords
- [ ] Add `{~ schema ~}` block for structured data
- [ ] Image alt text describes content + keyword
- [ ] Content length > 1500 words for pillar pages
- [ ] Include `{~ meta ~}` block for quick descriptions

Example markdown file structure:
```markdown
{~ seo
   title="Recursive Absurdism: Philosophy for the Digital Age"
   description="Exploring recursive absurdism, where we build systems that build us, creating new existential loops"
   keywords="recursive absurd, Mathew Storm, digital philosophy"
~}

# Recursive Absurdism and the Digital Condition

{~ meta description="We no longer discover absurdity; we manufacture it through recursive systems." ~}

Your content here...
```

## Phase 4: Authority Building (Weeks 5-8)

### 4.1 Backlink Acquisition Strategy

**Tier 1 Targets (High Authority)**
- Philosophy blogs/magazines
- AI/Tech philosophy publications
- Django/Python community sites
- Academic philosophy departments

**Tier 2 Targets (Niche Relevant)**
- Existentialism forums
- AI ethics discussions
- Software engineering blogs
- Canadian tech publications

**Outreach Templates**
```
Subject: The Recursive Absurd - A New Framework for Understanding Digital Existence

Hi [Name],

I've developed a philosophical framework called "recursive absurdism" that extends Camus' work into the digital age. It explores how we create systems that create us, leading to new forms of existential loops.

Given your interest in [their topic], I thought this might resonate with your audience. The concept is detailed at: https://mathewstorm.ca/philosophy/recursive-absurd/

Would you be interested in:
1. A guest post exploring this concept?
2. An interview about philosophy in the age of AI?
3. Collaboration on related topics?

Best,
Mathew Storm
```

### 4.2 Social Signals & Brand Building

```python
# Add social sharing metadata
def add_social_context(request):
    return {
        'social_links': {
            'twitter_share': f"https://twitter.com/intent/tweet?url={request.build_absolute_uri()}&text={title}",
            'linkedin_share': f"https://www.linkedin.com/sharing/share-offsite/?url={request.build_absolute_uri()}",
            'mastodon_share': f"https://mastodon.social/share?text={title}%20{request.build_absolute_uri()}",
        }
    }
```

## Phase 5: Technical Performance (Week 6)

### 5.1 Core Web Vitals Optimization

```python
# settings.py optimizations
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Minification
MINIFY_HTML = True

# Cache headers
WHITENOISE_MAX_AGE = 31536000  # 1 year
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br']

# Database optimization
CONN_MAX_AGE = 60
```

### 5.2 Image Optimization

```python
# Use WebP with fallbacks
class OptimizedImageField(models.ImageField):
    def save(self, *args, **kwargs):
        # Convert to WebP
        # Generate responsive sizes
        # Add lazy loading
        super().save(*args, **kwargs)
```

## Phase 6: Monitoring & Analytics (Ongoing)

### 6.1 Essential Tools Setup

1. **Google Search Console**
   - Verify domain ownership
   - Submit sitemap
   - Monitor index coverage
   - Track search queries

2. **Google Analytics 4**
   - Track user behavior
   - Monitor content performance
   - Set up conversion goals

3. **Schema Testing**
   - Use Google's Rich Results Test
   - Validate structured data

### 6.2 KPI Tracking

```python
# analytics/seo_metrics.py
class SEOMetrics(models.Model):
    date = models.DateField()
    keyword = models.CharField(max_length=100)
    position = models.IntegerField()
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    ctr = models.FloatField()

    class Meta:
        unique_together = ['date', 'keyword']
```

## Implementation Roadmap for Django Spellbook

### Week 1: Technical Foundation
- [ ] Implement SpellbookContentSitemap in `_core/sitemaps.py`
- [ ] Create robots.txt view in `A_base/views.py`
- [ ] Add Person schema to `A_base/templates/A_base/base.html`
- [ ] Set up Google Search Console
- [ ] Submit sitemap to Google

### Week 2: SpellBlock SEO System
- [ ] Create SEO SpellBlocks in `A_base/spellblocks.py`
- [ ] Create templates in `A_base/templates/A_base/blocks/`
- [ ] Run `python manage.py spellbook_md` to regenerate
- [ ] Add SEO blocks to philosophy content (recursive-absurd.md, etc.)
- [ ] Add SEO blocks to blog content

### Week 3-4: Content & About App
- [ ] Create 'about' Django app
- [ ] Create 'about_content' directory
- [ ] Add about app to settings.py arrays
- [ ] Write mathew-storm.md with full SEO
- [ ] Run `python manage.py spellbook_md`

### Week 5-6: Authority Building
- [ ] Update GitHub profile and repos
- [ ] Submit to directories
- [ ] Create disambiguation content
- [ ] Begin backlink outreach

### Week 7-8: Performance & Monitoring
- [ ] Verify WhiteNoise compression (already configured)
- [ ] Check analytics middleware
- [ ] Set up Google Analytics
- [ ] Monitor Search Console data

## Quick Wins with Django Spellbook (Do Today)

1. **Create SEO SpellBlocks in A_base/spellblocks.py**
   - Copy the SEO SpellBlock code from Phase 2
   - Create the template files
   - Run `python manage.py spellbook_md` to regenerate

2. **Add SEO blocks to existing markdown files:**
```markdown
{~ seo
   title="Your Page Title | Mathew Storm"
   description="Your 155-character description"
   keywords="your, keywords, here"
~}
```

3. **Verify Google Search Console:**
```html
<meta name="google-site-verification" content="your-verification-code" />
```

4. **Create 'about' app with Django Spellbook:**

   ```bash
   # Create the app and content directory
   python manage.py startapp about
   mkdir about_content

   # Create markdown files
   touch about_content/intro.md
   touch about_content/mathew-storm.md
   touch about_content/concepts.md
   touch about_content/contact.md
   ```

   Update `_core/settings.py`:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       "about",  # Add this
   ]

   SPELLBOOK_MD_PATH = [
       BASE_DIR / "projects_content",
       BASE_DIR / "tutorials_content",
       BASE_DIR / "blog_content",
       BASE_DIR / "notes_content",
       BASE_DIR / "philo_content",
       BASE_DIR / "about_content",  # Add this
   ]

   SPELLBOOK_MD_APP = [
       "projects",
       "tutorials",
       "blog",
       "notes",
       "philo",
       "about",  # Add this
   ]

   SPELLBOOK_MD_URL_PREFIX = [
       "proj",
       "tuts",
       "blog",
       "note",
       "philo",
       "about",  # Add this
   ]
   ```

   Then run: `python manage.py spellbook_md`

5. **Submit to directories:**
   - Google Business Profile (as author/philosopher)
   - GitHub profile update with keywords
   - LinkedIn optimization

## Success Metrics

**3 Months:**
- Ranking #1 for "Mathew Storm"
- Ranking #1 for "recursive absurd"
- 50+ indexed pages
- 10+ quality backlinks

**6 Months:**
- Top 10 for "AI assisted engineering"
- Featured snippet for philosophical concepts
- 100+ organic visitors/month
- Knowledge panel appearance

**12 Months:**
- Recognized authority on recursive absurdism
- Speaking opportunities from search visibility
- 500+ organic visitors/month
- Multiple keywords in position 1-3

## Resources & Tools

### Essential (Free)
- Google Search Console
- Google Analytics
- Schema.org validator
- GTmetrix for speed testing

### Recommended (Paid)
- Ahrefs or SEMrush for keyword research
- Screaming Frog for technical audits
- Surfer SEO for content optimization

### Django SEO Packages
```bash
pip install django-meta  # Meta tags management
pip install django-seo2  # SEO fields for models
pip install django-robots  # Robots.txt management
```

## Django Spellbook SEO Advantages

Django Spellbook gives you unique SEO superpowers:

1. **SpellBlocks = SEO at the Source**: Embed metadata directly in markdown where content lives
2. **Auto-generated Structure**: URL patterns and navigation created automatically
3. **Consistent Implementation**: SpellBlocks ensure every page has proper SEO
4. **Content-First Approach**: Write markdown, get optimized HTML automatically

## Final Notes

Your combination of unique philosophical concepts + Django Spellbook creates an unbeatable SEO advantage:

- **Zero competition** for "recursive absurd", "neo-absurdism", "80-20 Human-in-the-Loop"
- **Technical edge** with Django Spellbook (you're also ranking for the framework itself)
- **Content velocity** - SpellBlocks make it fast to create SEO-optimized content
- **Semantic relationships** - Spellbook's navigation automatically creates topical clusters

The winning formula:
1. Create markdown with SEO SpellBlocks
2. Run `python manage.py spellbook_md`
3. Django Spellbook handles the rest
4. Your unique concepts dominate search

Remember: With Django Spellbook, SEO becomes part of your writing workflow, not a separate technical task. Every markdown file you create is automatically SEO-optimized.