from django.contrib import admin
from .models import TutorialTitle, Question
from django.utils.html import format_html # For potential custom display

class QuestionInline(admin.TabularInline): # Or admin.StackedInline for a different layout
    model = Question
    fk_name = 'tutorial_title' # Explicitly state the foreign key field
    fields = ('question_id_slug', 'question_text_preview', 'difficulty', 'correct_answer') # Keep inline form concise
    readonly_fields = ('question_text_preview',)
    extra = 1  # How many empty forms for new questions to show
    show_change_link = True # Allows linking to the full Question change form

    def question_text_preview(self, obj):
        if obj.pk: # Check if object exists (i.e., not an empty new form)
            return (obj.question_text[:70] + '...') if len(obj.question_text) > 70 else obj.question_text
        return "-"
    question_text_preview.short_description = 'Question Preview'

@admin.register(TutorialTitle)
class TutorialTitleAdmin(admin.ModelAdmin):
    list_display = ('title_id_slug', 'name', 'question_count') # Added question_count
    search_fields = ('title_id_slug', 'name')
    ordering = ('title_id_slug',)
    list_per_page = 25
    inlines = [QuestionInline] # <-- Here's the inline!

    def question_count(self, obj):
        # This is a custom function for list_display
        return obj.questions.count()
    question_count.short_description = 'No. of Questions'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # More concise and informative list display
    list_display = (
        'question_id_slug',
        'short_question_text', # Custom method for preview
        'tutorial_title_link', # Custom method for clickable link
        'difficulty',
        'correct_answer_display', # Custom method for better display
        'display_tags',        # Custom method to show tags
        'updated_at',
    )
    list_filter = ('difficulty', 'tutorial_title', 'tags') # Added tutorial_title and tags
    search_fields = (
        'question_id_slug',
        'question_text',
        'answer_a', 'answer_b', 'answer_c', 'answer_d', # Keep these if direct answer search is needed
        'tutorial_title__title_id_slug', # Search by related field
        'tutorial_title__name',
        'tags__name', # Search by tag name (django-taggit)
    )
    ordering = ('tutorial_title', 'question_id_slug')
    list_per_page = 20
    # Use raw_id_fields if you have many TutorialTitle instances
    raw_id_fields = ('tutorial_title',) 

    fieldsets = (
        (None, {
            'fields': ('tutorial_title', 'question_id_slug', 'question_text')
        }),
        ('Answer Options', {
            'classes': ('collapse',), # Optional: make this section collapsible
            'fields': (('answer_a', 'answer_b'), 
                       ('answer_c', 'answer_d'), 
                       'correct_answer')
        }),
        ('Categorization & Metadata', {
            'fields': ('difficulty', 'tags')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def short_question_text(self, obj):
        """Creates a truncated version of the question text for list_display."""
        return (obj.question_text[:70] + '...') if len(obj.question_text) > 70 else obj.question_text
    short_question_text.short_description = 'Question (Preview)'

    def display_tags(self, obj):
        """Displays tags as a comma-separated string."""
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'

    def correct_answer_display(self, obj):
        """Displays the correct answer choice's label."""
        return obj.get_correct_answer_display() # Uses the get_FOO_display() for choice fields
    correct_answer_display.short_description = 'Correct Answer'
    correct_answer_display.admin_order_field = 'correct_answer'


    def tutorial_title_link(self, obj):
        """Makes the tutorial_title clickable in the list_display."""
        from django.urls import reverse
        link = reverse("admin:questions_tutorialtitle_change", args=[obj.tutorial_title.pk])
        return format_html('<a href="{}">{}</a>', link, obj.tutorial_title)
    tutorial_title_link.short_description = 'Tutorial Title'
    tutorial_title_link.admin_order_field = 'tutorial_title'