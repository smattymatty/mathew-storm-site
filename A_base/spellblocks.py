from django_spellbook.blocks import BasicSpellBlock, SpellBlockRegistry
import logging # For potential warnings/errors

logger = logging.getLogger(__name__) # Or a more specific logger

@SpellBlockRegistry.register()
class ParamaterSpellBlock(BasicSpellBlock):
    name = "parameter_v1"
    template = "A_base/blocks/parameter_v1.html" # Main template for the hero block
    
    def get_context(self):
        """
        Get the name, type, and description of the parameter.
        """
        context = super().get_context() # Gets basic context like 'content', 'kwargs'
        
        context["name"] = self.kwargs.get("name")
        context["type"] = self.kwargs.get("type")
        
        return context

@SpellBlockRegistry.register()
class LabelSeperatorSpellBlock(BasicSpellBlock):
    name = "label_seperator"
    template = "A_base/blocks/label_seperator.html" # Main template for the hero block

    DEFAULT_ALIGN = "center"
    DEFAULT_COLOR = "info-75" # color effects the text and border
    DEFAULT_BG_COLOR = "white-75"

    def get_context(self):
        """
        Extends the template context with alignment, color, and background color settings.
        
        Adds 'align', 'color', and 'bg_color' keys to the context dictionary, using values
        from the block's keyword arguments or falling back to class defaults if not provided.
        The alignment value is converted to lowercase.
        """
        context = super().get_context() # Gets basic context like 'content', 'kwargs'
        
        context["align"] = self.kwargs.get("align", self.DEFAULT_ALIGN).lower()
        context["color"] = self.kwargs.get("color", self.DEFAULT_COLOR)
        context["bg_color"] = self.kwargs.get("bg_color", self.DEFAULT_BG_COLOR)

        return context

@SpellBlockRegistry.register()
class CarouselBlock(BasicSpellBlock):
    name = "carousel"
    template = "A_base/blocks/carousel.html"

    def get_context(self):
        """
        Process image URLs, descriptions, and links into a list for template iteration.
        Supports up to 5 images with descriptions and optional links.
        """
        context = super().get_context()

        # Collect images, descriptions, and links
        images = []
        for i in range(1, 6):  # Support up to 5 images
            image_url = self.kwargs.get(f'image{i}')
            if image_url:
                images.append({
                    'url': image_url,
                    'description': self.kwargs.get(f'image{i}desc', f'Image {i}'),
                    'link': self.kwargs.get(f'image{i}link', ''),  # Optional link
                    'index': i - 1  # Zero-based index for JavaScript
                })

        context['images'] = images
        context['carousel_id'] = f"carousel-{id(self)}"  # Unique ID for multiple carousels

        return context

@SpellBlockRegistry.register()
class SkillCategoryBlock(BasicSpellBlock):
    name = "skill_category"
    template = "A_base/blocks/skill_category.html"

    def get_context(self):
        """
        Process skill category data with experience levels and highlights.
        Skills format: "skill:years:level" separated by pipes
        Example: "Python:5:expert|Django:5:expert|PostgreSQL:4:advanced"
        """
        context = super().get_context()

        # Get category name and icon
        context['category_name'] = self.kwargs.get('name', 'Skills')
        context['icon'] = self.kwargs.get('icon', 'code')  # Default icon
        context['highlight'] = self.kwargs.get('highlight', '')  # Featured skill to highlight

        # Parse skills string
        skills_raw = self.kwargs.get('skills', '')
        skills = []

        if skills_raw:
            for skill_str in skills_raw.split('|'):
                parts = skill_str.split(':')
                skill_data = {
                    'name': parts[0] if len(parts) > 0 else skill_str,
                    'years': parts[1] if len(parts) > 1 else '',
                    'level': parts[2] if len(parts) > 2 else 'intermediate'
                }

                # Add visual level indicators
                if skill_data['level'] == 'expert':
                    skill_data['level_dots'] = 5
                    skill_data['level_color'] = 'success'
                elif skill_data['level'] == 'advanced':
                    skill_data['level_dots'] = 4
                    skill_data['level_color'] = 'primary'
                else:  # intermediate
                    skill_data['level_dots'] = 3
                    skill_data['level_color'] = 'secondary'

                # Check if this skill should be highlighted
                skill_data['is_highlighted'] = skill_data['name'].lower() in context['highlight'].lower()

                skills.append(skill_data)

        context['skills'] = skills
        context['skill_category_id'] = f"skills-{id(self)}"  # Unique ID

        return context

@SpellBlockRegistry.register()
class ProjectShowcaseBlock(BasicSpellBlock):
    name = "project_showcase"
    template = "A_base/blocks/project_showcase.html"

    def get_context(self):
        """
        Process project showcase data with all details for professional display.
        Supports title, subtitle, description, highlights, tech stack, stats, and links.
        """
        context = super().get_context()

        # Basic project info
        context['title'] = self.kwargs.get('title', 'Project')
        context['subtitle'] = self.kwargs.get('subtitle', '')
        context['description'] = self.kwargs.get('description', '')

        # Project type for visual styling
        context['project_type'] = self.kwargs.get('type', 'default')  # default, saas, opensource, team

        # Highlights or key features (pipe-separated)
        highlights_raw = self.kwargs.get('highlights', '')
        context['highlights'] = [h.strip() for h in highlights_raw.split('|')] if highlights_raw else []

        # Alternative: use section_title and section_items for flexibility
        context['section_title'] = self.kwargs.get('section_title', 'Key Features')

        # Tech stack (pipe-separated)
        tech_raw = self.kwargs.get('tech', '')
        context['tech_stack'] = [t.strip() for t in tech_raw.split('|')] if tech_raw else []

        # Statistics (format: "label:value|label:value")
        stats_raw = self.kwargs.get('stats', '')
        stats = []
        if stats_raw:
            for stat_str in stats_raw.split('|'):
                parts = stat_str.split(':')
                if len(parts) == 2:
                    stats.append({
                        'label': parts[0].strip(),
                        'value': parts[1].strip()
                    })
        context['stats'] = stats

        # Links
        context['primary_link'] = self.kwargs.get('primary_link', '')
        context['primary_link_text'] = self.kwargs.get('primary_link_text', 'View Project')
        context['github_link'] = self.kwargs.get('github_link', '')
        context['docs_link'] = self.kwargs.get('docs_link', '')

        # Optional image
        context['image_url'] = self.kwargs.get('image', '')
        context['image_link'] = self.kwargs.get('image_link', context['primary_link'])

        # Featured flag for special styling
        context['is_featured'] = self.kwargs.get('featured', '').lower() == 'true'

        # Unique ID for animations
        context['project_id'] = f"project-{id(self)}"

        return context

@SpellBlockRegistry.register()
class AchievementBlock(BasicSpellBlock):
    name = "achievement"
    template = "A_base/blocks/achievement.html"

    def get_context(self):
        """
        Process achievement/experience data for professional display.
        Supports title, icon, achievements list with optional metrics.
        """
        context = super().get_context()

        # Basic info
        context['title'] = self.kwargs.get('title', 'Achievement')
        context['icon'] = self.kwargs.get('icon', 'star')  # star, code, lightbulb, users, book, chart, trophy

        # Color theme
        context['color_theme'] = self.kwargs.get('color', 'primary')  # primary, success, accent, secondary

        # Parse achievements (pipe-separated)
        achievements_raw = self.kwargs.get('items', '')
        achievements = []

        if achievements_raw:
            for achievement_str in achievements_raw.split('|'):
                # Check if there's a metric in the format "metric:description"
                # e.g., "5+ years:Python/Django production experience"
                parts = achievement_str.split(':', 1)

                if len(parts) == 2 and any(char.isdigit() for char in parts[0]):
                    # Has a metric
                    achievements.append({
                        'metric': parts[0].strip(),
                        'text': parts[1].strip(),
                        'has_metric': True
                    })
                else:
                    # No metric, just text
                    achievements.append({
                        'text': achievement_str.strip(),
                        'has_metric': False
                    })

        context['achievements'] = achievements

        # Optional: featured flag for special styling
        context['is_featured'] = self.kwargs.get('featured', '').lower() == 'true'

        # Unique ID for animations
        context['achievement_id'] = f"achievement-{id(self)}"

        return context