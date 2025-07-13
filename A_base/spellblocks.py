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