# 3-Phase SEO Implementation Plan

## PHASE 1: Technical Foundation & Google Discovery (2-3 hours)
**Goal: Get Google to find and understand your site**

### Step 1: Sitemap Implementation (30 min)
1. Create `_core/sitemaps.py` with SpellbookContentSitemap
2. Update `_core/urls.py` to add sitemap.xml route
3. Test at https://mathewstorm.ca/sitemap.xml

### Step 2: Robots.txt (15 min)
1. Add robots_txt view to `A_base/views.py`
2. Update `A_base/urls.py` with robots.txt route
3. Verify at https://mathewstorm.ca/robots.txt

### Step 3: Structured Data (30 min)
1. Add Person schema to `A_base/templates/A_base/base.html`
2. Include your actual GitHub/LinkedIn URLs
3. Test with Google's Rich Results Test

### Step 4: Google Setup (1 hour)
1. Verify site in Google Search Console
2. Submit sitemap
3. Request indexing for homepage
4. Check coverage report

**Success Metric:** Site indexed in Google within 48 hours

### Implementation Code for Phase 1

#### Sitemap (_core/sitemaps.py)
```python
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pathlib import Path
from django.conf import settings

class SpellbookContentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        items = []
        for idx, content_path in enumerate(settings.SPELLBOOK_MD_PATH):
            app_name = settings.SPELLBOOK_MD_APP[idx]
            for md_file in Path(content_path).glob('**/*.md'):
                relative_path = md_file.relative_to(content_path)
                url_path = str(relative_path).replace('.md', '').replace('\\', '/')
                if url_path == 'intro':
                    url_path = ''
                items.append(f"{app_name}:{url_path}" if url_path else f"{app_name}:intro")
        return items

    def location(self, item):
        try:
            return reverse(item)
        except:
            return '/'

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['A_base:home', 'questions:questions_page']

    def location(self, item):
        return reverse(item)
```

#### Robots.txt (A_base/views.py)
```python
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
```

---

## PHASE 2: SEO SpellBlock System (1-2 hours)
**Goal: Make every piece of content SEO-optimized**

### Step 1: Create SpellBlocks (30 min)
1. Create `A_base/spellblocks.py` with SEO, Meta, Schema blocks
2. Create template files in `A_base/templates/A_base/blocks/`
3. Run `python manage.py spellbook_md`

### Step 2: Optimize Top Content (45 min)
Add SEO blocks to your 5 most important files:
1. `philo_content/the-recursive-absurd.md`
2. `philo_content/techno-absurdism.md`
3. `blog_content/Artificial_Intelligence/vibe Coding vs AI Assisted Engineering.md`
4. `philo_content/humanist-absurdism.md`
5. `philo_content/neo-absurdism.md`

### Step 3: Regenerate Site (15 min)
1. Run `python manage.py spellbook_md`
2. Test pages to verify SEO metadata
3. Check meta tags in browser inspector

**Success Metric:** All key pages have proper meta descriptions

### Implementation Code for Phase 2

#### SpellBlocks (A_base/spellblocks.py)
```python
from django_spellbook.blocks import BasicSpellBlock, SpellBlockRegistry

@SpellBlockRegistry.register()
class SEOBlock(BasicSpellBlock):
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
    name = 'meta'
    template = 'A_base/blocks/meta_description.html'

    def get_context(self):
        context = super().get_context()
        context['description'] = self.kwargs.get('description', self.content[:155])
        return context

@SpellBlockRegistry.register()
class SchemaBlock(BasicSpellBlock):
    name = 'schema'
    template = 'A_base/blocks/schema_article.html'

    def get_context(self):
        context = super().get_context()
        context['type'] = self.kwargs.get('type', 'Article')
        context['headline'] = self.kwargs.get('headline', '')
        context['date'] = self.kwargs.get('date', '')
        return context
```

#### Example Markdown with SEO
```markdown
{~ seo
   title="The Recursive Absurd - Mathew Storm's Philosophy"
   description="Discover recursive absurdism: where we build systems that build us. A new philosophical framework by Mathew Storm."
   keywords="recursive absurd, recursive absurdism, Mathew Storm, digital philosophy"
~}

# The Recursive Absurd: A Digital Addendum to Sisyphus

[Your existing content...]
```

---

## PHASE 3: About App & Personal Brand (2-3 hours)
**Goal: Establish "Mathew Storm" as primary entity**

### Step 1: Create About App (30 min)
```bash
python manage.py startapp about
mkdir about_content
```

Update `_core/settings.py`:
```python
INSTALLED_APPS = [
    # ... existing apps
    "about",
]

SPELLBOOK_MD_PATH = [
    # ... existing paths
    BASE_DIR / "about_content",
]

SPELLBOOK_MD_APP = [
    # ... existing apps
    "about",
]

SPELLBOOK_MD_URL_PREFIX = [
    # ... existing prefixes
    "about",
]
```

### Step 2: Write Key Pages (1.5 hours)

#### about_content/mathew-storm.md
```markdown
{~ seo
   title="Mathew Storm - Software Developer & Philosophical Author"
   description="Mathew Storm: Founder of 80-20 Human-in-the-Loop, creator of recursive absurdism. NOT the basketball player."
   keywords="Mathew Storm, recursive absurd, 80-20 Human-in-the-Loop, Django developer, philosophical author"
~}

# Mathew Storm

**Not the basketball player.** Software developer, philosophical author, and creator of recursive absurdism.

## Who is Mathew Storm?

I'm Mathew Storm, a Canadian software developer and philosophical author. I founded the 80-20 Human-in-the-Loop community and created the philosophical framework of recursive absurdism.

## My Work

- **Recursive Absurdism**: A philosophy exploring how we build systems that build us
- **Django Spellbook**: Open-source markdown CMS for Django
- **80-20 Human-in-the-Loop**: Methodology where humans lead, AI amplifies

## Not to Be Confused With

- Mathew Storms (basketball player)
- Firefly (Marvel character)
- Hurricane Matthew

Visit [mathewstorm.ca](https://mathewstorm.ca) for more.
```

### Step 3: External Optimization (1 hour)
1. Update GitHub bio
2. Create GitHub profile README
3. Update LinkedIn headline
4. Submit to Google Knowledge Panel

**Success Metric:** "Mathew Storm" search shows your site in top 3

---

## Implementation Schedule

**Day 1 (Today):** Phase 1 - Technical Foundation
- Morning: Sitemap & robots.txt
- Afternoon: Structured data & Google Search Console

**Day 2:** Phase 2 - SEO SpellBlocks
- Create SpellBlock system
- Add to existing content

**Day 3-4:** Phase 3 - About App
- Build about section
- External profile optimization

**Day 5:** Monitoring
- Check Google Search Console
- Verify indexing
- Test searches

## Quick Command Reference

```bash
# After Phase 1
python manage.py runserver  # Test sitemap/robots

# After Phase 2
python manage.py spellbook_md  # Regenerate with SEO

# After Phase 3
python manage.py startapp about
python manage.py spellbook_md
```

## Validation Checkpoints

✅ **Phase 1 Complete When:**
- [ ] https://mathewstorm.ca/sitemap.xml loads
- [ ] https://mathewstorm.ca/robots.txt loads
- [ ] Google Search Console verified
- [ ] Sitemap submitted to Google

✅ **Phase 2 Complete When:**
- [ ] SEO SpellBlocks created
- [ ] Top 5 content files have SEO blocks
- [ ] Meta tags visible in browser inspector
- [ ] `python manage.py spellbook_md` runs without errors

✅ **Phase 3 Complete When:**
- [ ] About app created and configured
- [ ] mathew-storm.md page live
- [ ] GitHub/LinkedIn profiles updated
- [ ] Google Knowledge Panel requested

## Troubleshooting

**Sitemap not loading?**
- Check `_core/urls.py` includes the sitemap import
- Verify `django.contrib.sitemaps` in INSTALLED_APPS

**SpellBlocks not rendering?**
- Ensure templates are in correct path
- Run `python manage.py spellbook_md` after changes
- Check for typos in block names

**About app not working?**
- Verify all 4 settings arrays updated
- Check `about_content` directory exists
- Run `python manage.py spellbook_md`

## Next Steps After Implementation

1. **Week 1**: Monitor Google Search Console daily
2. **Week 2**: Add SEO blocks to remaining content
3. **Month 1**: Track keyword rankings
4. **Month 3**: Evaluate and adjust strategy

Remember: SEO is a marathon. These phases lay the foundation for long-term dominance of "Mathew Storm" and "recursive absurd" searches.