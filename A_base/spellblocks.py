from django_spellbook.blocks import BasicSpellBlock, SpellBlockRegistry
import logging

logger = logging.getLogger(__name__)

@SpellBlockRegistry.register()
class ProjectCard(BasicSpellBlock):
    """Elegant project showcase card for Storm Developments projects"""
    name = "project_card"
    template = "A_base/blocks/project_card.html"
    
    def get_context(self):
        context = super().get_context()
        
        # Basic project info
        context['title'] = self.kwargs.get('title', 'Project')
        context['description'] = self.kwargs.get('description', '')
        context['status'] = self.kwargs.get('status', '')
        
        # Project identifier for accent color (storm-cloud, spellbook, mercury)
        context['project'] = self.kwargs.get('project', '')
        
        # Links
        context['github_link'] = self.kwargs.get('github', '')
        context['pypi_link'] = self.kwargs.get('pypi', '')
        context['docs_link'] = self.kwargs.get('docs', '')
        context['live_link'] = self.kwargs.get('live', '')
        
        # Stats (pipe-separated format: "label:value|label:value")
        stats_raw = self.kwargs.get('stats', '')
        stats = []
        if stats_raw:
            for stat_str in stats_raw.split('|'):
                parts = stat_str.split(':', 1)
                if len(parts) == 2:
                    stats.append({
                        'label': parts[0].strip(),
                        'value': parts[1].strip()
                    })
        context['stats'] = stats
        
        # Tech stack (pipe-separated)
        tech_raw = self.kwargs.get('tech', '')
        context['tech_stack'] = [t.strip() for t in tech_raw.split('|')] if tech_raw else []
        
        return context


@SpellBlockRegistry.register()
class TechStack(BasicSpellBlock):
    """Display technology stack in a clean list"""
    name = "tech_stack"
    template = "A_base/blocks/tech_stack.html"
    
    def get_context(self):
        context = super().get_context()
        
        # Technologies (pipe-separated)
        tech_raw = self.kwargs.get('technologies', '')
        context['technologies'] = [t.strip() for t in tech_raw.split('|')] if tech_raw else []
        context['title'] = self.kwargs.get('title', 'Tech Stack')
        
        return context


@SpellBlockRegistry.register()
class StormHeroBlock(BasicSpellBlock):
    """Epic hero section with Storm Lightning animations"""
    name = "storm_hero"
    template = "A_base/blocks/storm_hero.html"
    
    def get_context(self):
        context = super().get_context()
        context['image'] = self.kwargs.get('image', '')
        context['title'] = self.kwargs.get('title', 'Mathew Storm')
        context['tagline'] = self.kwargs.get('tagline', '')
        context['cta_text'] = self.kwargs.get('cta_text', 'View Projects')
        context['cta_link'] = self.kwargs.get('cta_link', '#projects')
        return context


@SpellBlockRegistry.register()
class SEOBlock(BasicSpellBlock):
    """SEO metadata SpellBlock for embedding meta tags in content"""
    name = 'seo'
    template = 'A_base/blocks/seo_metadata.html'

    def get_context(self):
        context = super().get_context()
        context['title'] = self.kwargs.get('title', '')
        context['description'] = self.kwargs.get('description', '')
        context['keywords'] = self.kwargs.get('keywords', '')
        context['author'] = self.kwargs.get('author', 'Mathew Storm')
        context['og_image'] = self.kwargs.get('image', '')
        context['og_type'] = self.kwargs.get('type', 'article')
        return context


@SpellBlockRegistry.register()
class MetaBlock(BasicSpellBlock):
    """Quick meta description block"""
    name = 'meta'
    template = 'A_base/blocks/meta_description.html'

    def get_context(self):
        context = super().get_context()
        context['description'] = self.kwargs.get('description', self.content[:155] if self.content else '')
        return context


@SpellBlockRegistry.register()
class SchemaBlock(BasicSpellBlock):
    """Structured data block for articles and other content types"""
    name = 'schema'
    template = 'A_base/blocks/schema_article.html'

    def get_context(self):
        context = super().get_context()
        context['schema_type'] = self.kwargs.get('type', 'Article')
        context['headline'] = self.kwargs.get('headline', '')
        context['date_published'] = self.kwargs.get('date', '')
        context['author'] = self.kwargs.get('author', 'Mathew Storm')
        context['description'] = self.kwargs.get('description', '')
        return context
