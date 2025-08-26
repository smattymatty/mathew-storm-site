"""Theme middleware for handling light/dark mode switching."""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ThemeMiddleware(MiddlewareMixin):
    """Apply theme configuration on each request based on session."""
    
    def process_request(self, request):
        """Apply theme from session or use default."""
        # Get mode from session, default to 'dark' (Bob Ross painted at night!)
        theme_mode = request.session.get('theme_mode', 'dark')
        
        # Apply the appropriate theme mode
        if hasattr(settings, 'EARTHTONE_THEME'):
            theme_config = settings.EARTHTONE_THEME['modes'].get(theme_mode, settings.EARTHTONE_THEME['modes']['dark'])
            settings.SPELLBOOK_THEME = theme_config
            
            # Store current mode in request for template access
            request.theme_mode = theme_mode
        
        return None