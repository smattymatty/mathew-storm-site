## What are Django Forms?
- Built-in feature that handles HTML forms
- Manages data validation, rendering, and processing
- Reduces repetitive code and improves security
- Supports both simple forms and model-backed forms
### Form Processing Flow
1. Display empty form on GET request
2. Receive submitted data on POST request
3. Validate the submitted data
4. If valid, process the data
5. If invalid, redisplay form with error messages

---

# Creating a Basic Contact Form

Create a new file: `A_base/forms.py`

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your message',
            'rows': 4
        })
    )
```

---

## Form Field Types

Django provides many field types for different data:

- CharField - Text with maximum length
- EmailField - Validates email format
- IntegerField - Validates integers
- DateField - Date input
- BooleanField - Checkbox input
- ChoiceField - Select dropdown
- FileField - File uploads
## Form Widgets

Widgets control how fields render in HTML:

- TextInput - Standard text field
- EmailInput - Email field with validation
- Textarea - Multiline text area
- Select - Dropdown menu
- CheckboxInput - Checkbox
- DateInput - Date picker

Customize with `attrs` dictionary

---

# Creating a Form View

Update `A_base/views.py`:

```python
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the valid form data
            print("VALID FORM DATA:")
            print(f"Name: {form.cleaned_data['name']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Message: {form.cleaned_data['message']}")
    else:
        form = ContactForm()

    return render(request, 'A_base/contact.html', {'form': form})
```

**request.method == ‘POST’:**  If the method is a post, that means it was sent by a form.

---

# Add URL for the Contact Form

Update `A_base/urls.py`:

```python
urlpatterns = [
    path("", views.base_view, name="base"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
]
```

---

# Create the Template

Create `A_base/templates/A_base/contact.html`:

```html
{% extends "A_base/base.html" %}

{% block content %}
<h1>Contact Us</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send Message</button>
</form>
{% endblock %}
```

---

# Form Rendering Options

Django offers several ways to render forms:

```html
{{ form.as_p }}    <!-- Wraps fields in <p> tags -->
{{ form.as_table }} <!-- Renders as table rows -->
{{ form.as_ul }}   <!-- Renders as list items -->
```

For custom rendering:

```html
<div>
    <label for="{{ form.name.id_for_label }}">Name:</label>
    {{ form.name }}
    {{ form.name.errors }}
</div>
```

---

# CSRF Protection

- `{% csrf_token %}` adds a hidden field with security token
- Protects against Cross-Site Request Forgery attacks
- Required in all POST forms in Django
- Django will reject form submissions without a valid token

---

# Form Validation

Django automatically validates:

- Required fields
- Field types (email format, integer values)
- Length constraints
- Custom validators

Access cleaned data after validation:

```python
if form.is_valid():
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    # Process data...
```

---

# Custom Form Validation

Add custom validation with `clean_fieldname` methods:

```python
class ContactForm(forms.Form):
    # Field definitions...
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise forms.ValidationError(
                "Only example.com email addresses allowed"
            )
        return email
```

---

# Form-wide Validation

Validate relationships between fields:

```python
class ContactForm(forms.Form):
    # Field definitions...
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        
        if name and name in message:
            raise forms.ValidationError(
                "Message cannot contain your name"
            )
        return cleaned_data
```

---
# Introduction to Model Forms

- Django forms directly tied to models
- Automatically create form fields from model fields
- Handle saving data to the database
- Reduce duplicate code between models and forms

Regular Form:

- Must define each field manually
- Requires custom code to save to database
- Good for forms not tied to models

Model Form:

- Fields generated from model
- Built-in `.save()` method
- Automatic validation based on model fields

# Level 1: Basic Model Forms

* Django ModelForms automatically create forms from your models
* Saves coding time and ensures form fields match model fields

```python
# A_projects/forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
```

* Fields are automatically generated based on model
* Field validation comes directly from model constraints
* Provides `.save()` method to create/update model instances

---

# Level 1: Using the Form in a View

* Create a view that handles both GET (show form) and POST (process form)

```python
# A_projects/views.py
from django.shortcuts import render, redirect
from .forms import ProjectForm

def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    
    return render(request, 'A_projects/create_project.html', {'form': form})
```

* GET requests show empty form, POST requests process submitted data
* `form.save()` creates a new Project instance in the database
* After successful save, redirect to the project detail page

---

# Level 1: Template for Project Form

* Create a template to display your form

```html
<!-- A_projects/templates/A_projects/create_project.html -->
{% extends "A_base/base.html" %}

{% block content %}
<h1>Create New Project</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Project</button>
</form>
{% endblock %}
```

* `form.as_p` renders each field wrapped in paragraph tags
* `{% csrf_token %}` adds security token to prevent CSRF attacks
* Add URL pattern in urls.py: `path("create/", views.create_project_view, name="create_project")`

---

# Level 2: Customizing Model Forms

* Add widgets, labels, help text, and other customizations

```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Project Name',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your project...',
                'rows': 4,
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Project Title',
        }
        help_texts = {
            'description': 'Provide details about project goals and scope.',
        }
```

* `widgets` customize the HTML input elements
* `labels` change the field labels displayed to users
* `help_texts` add explanatory text below fields

---

# Level 2: Custom Field Validation

* Add custom validation to specific fields

```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        # widgets, labels, etc...
    
    def clean_name(self):
        """Validate the name field."""
        name = self.cleaned_data['name']
        
        # Check if name contains project
        if 'project' not in name.lower():
            raise forms.ValidationError(
                "Name should contain the word 'project'"
            )
            
        return name
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        description = cleaned_data.get('description', '')
        
        if name and description and name in description:
            raise forms.ValidationError(
                "Description should not repeat the project name"
            )
            
        return cleaned_data
```

* `clean_fieldname` methods validate individual fields
* `clean` method validates relationships between fields

---

# Level 3: Many-to-Many Relationships

* Handle the Project-TeamMember many-to-many relationship

```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']
        widgets = {
            # Previous widgets...
            'members': forms.CheckboxSelectMultiple()
        }
```

* `CheckboxSelectMultiple` displays all TeamMembers as checkboxes
* Users can select multiple members to assign to the project
* Django automatically handles the many-to-many relationship

---

# Level 3: Enhanced Member Selection

* Filter available members and customize the display

```python
from A_base.models import TeamMember

class ProjectForm(forms.ModelForm):
    # Create a custom field replacing the model's field
    members = forms.ModelMultipleChoiceField(
        queryset=TeamMember.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text="Select team members to assign to this project"
    )
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'members']
        # Other customizations...
```

* `ModelMultipleChoiceField` provides more control than automatic field
* Can filter the queryset to show only certain members
* `order_by('name')` sorts members alphabetically for easier selection

---

# Level 4: Introduction to FormSets

* FormSets manage multiple instances of the same form
* Perfect for creating multiple Tasks for a Project at once

```python
from django.forms import modelformset_factory
from .models import Task

# Create a formset factory for Task forms
TaskFormSet = modelformset_factory(
    Task,
    fields=('name', 'description', 'status', 'due_date'),
    extra=3,  # Show 3 empty forms
    can_delete=True  # Allow deleting tasks
)
```

* `modelformset_factory` creates a class for managing multiple model forms
* `extra=3` provides three empty forms for new tasks
* `can_delete=True` adds a checkbox to delete existing tasks

---

# Level 4: Using FormSets in Views

* Integrate the TaskFormSet in a view

```python
def manage_tasks_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Filter tasks to show only those for this project
    TaskFormSet = modelformset_factory(
        Task,
        fields=('name', 'status', 'due_date'),
        extra=2
    )
    
    if request.method == 'POST':
        formset = TaskFormSet(
            request.POST,
            queryset=Task.objects.filter(project=project)
        )
        
        if formset.is_valid():
            # Set the project for each new task
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = project
                instance.save()
            
            # Handle deleted forms
            formset.save_m2m()
            
            return redirect('project_detail', slug=project.slug)
    else:
        formset = TaskFormSet(queryset=Task.objects.filter(project=project))
    
    return render(request, 'A_projects/manage_tasks.html', {
        'formset': formset,
        'project': project
    })
```

* `queryset` filters tasks to show only those for the current project
* `save(commit=False)` allows setting the project before saving
* `save_m2m()` saves any many-to-many relationships

---

# Level 4: FormSet Template

* Display multiple forms in the template

```html
<!-- A_projects/templates/A_projects/manage_tasks.html -->
{% extends "A_base/base.html" %}

{% block content %}
<h1>Manage Tasks for {{ project.name }}</h1>

<form method="post">
    {% csrf_token %}
    {{ formset.management_form }}
    
    <table>
        <thead>
            <tr>
                <th>Task Name</th>
                <th>Status</th>
                <th>Due Date</th>
                {% if formset.can_delete %}
                <th>Delete</th>
                {% endif %}
            </tr>
        </thead>
        <tbody>
            {% for form in formset %}
            <tr>
                <td>
                    {{ form.id }}
                    {{ form.name }}
                    {{ form.name.errors }}
                </td>
                <td>
                    {{ form.status }}
                    {{ form.status.errors }}
                </td>
                <td>
                    {{ form.due_date }}
                    {{ form.due_date.errors }}
                </td>
                {% if formset.can_delete %}
                <td>{{ form.DELETE }}</td>
                {% endif %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <button type="submit">Save Tasks</button>
</form>
{% endblock %}
```

* `{{ formset.management_form }}` is required for formset functionality
* Loop through each form to display fields
* Include hidden `id` field to track existing tasks

---

# Level 5: Inline FormSets

* Create forms for related models (Task forms inside Project form)

```python
from django.forms import inlineformset_factory

# Create an inline formset for Tasks within a Project
TaskInlineFormSet = inlineformset_factory(
    Project,  # Parent model
    Task,     # Child model
    fields=('name', 'status', 'due_date'),
    extra=2,
    can_delete=True
)
```

* `inlineformset_factory` creates forms for related models
* Parent-child relationship is automatically handled
* Tasks will be properly associated with the Project

---

# Level 5: Using Inline FormSets

* Combined Project form and multiple Task forms

```python
def create_project_with_tasks_view(request):
    if request.method == 'POST':
        # Process the project form
        project_form = ProjectForm(request.POST)
        
        if project_form.is_valid():
            # Save the project first
            project = project_form.save()
            
            # Process the task formset
            task_formset = TaskInlineFormSet(request.POST, instance=project)
            
            if task_formset.is_valid():
                task_formset.save()
                return redirect('project_detail', slug=project.slug)
    else:
        # Display empty forms
        project_form = ProjectForm()
        task_formset = TaskInlineFormSet()
    
    return render(request, 'A_projects/create_project_with_tasks.html', {
        'project_form': project_form,
        'task_formset': task_formset
    })
```

* Use `instance=project` to connect tasks to the project
* Both project form and task formset must be valid
* All forms are submitted in a single request

---

# Level 5: Editing Projects with Tasks

* Similar approach for editing existing projects and tasks

```python
def edit_project_with_tasks_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        task_formset = TaskInlineFormSet(
            request.POST, 
            instance=project
        )
        
        if project_form.is_valid() and task_formset.is_valid():
            project_form.save()
            task_formset.save()
            return redirect('project_detail', slug=project.slug)
    else:
        project_form = ProjectForm(instance=project)
        task_formset = TaskInlineFormSet(instance=project)
    
    return render(request, 'A_projects/edit_project_with_tasks.html', {
        'project_form': project_form,
        'task_formset': task_formset,
        'project': project
    })
```

* `instance=project` pre-fills forms with existing data
* Both forms and formsets accept an `instance` parameter
* Same template structure can be used for create and edit

---

# Level 5: Combined Template

* Display project form and task formset together

```html
<!-- A_projects/templates/A_projects/create_project_with_tasks.html -->
{% extends "A_base/base.html" %}

{% block content %}
<h1>Create Project with Tasks</h1>

<form method="post">
    {% csrf_token %}
    
    <h2>Project Details</h2>
    {{ project_form.as_p }}
    
    <h2>Tasks</h2>
    {{ task_formset.management_form }}
    
    <table>
        <thead>
            <tr>
                <th>Task Name</th>
                <th>Status</th>
                <th>Due Date</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            {% for form in task_formset %}
            <tr>
                <td>
                    {{ form.id }}
                    {{ form.name }}
                </td>
                <td>{{ form.status }}</td>
                <td>{{ form.due_date }}</td>
                <td>{{ form.DELETE }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <button type="submit">Save Project with Tasks</button>
</form>
{% endblock %}
```

* Project form and task formset in a single form
* Both submitted with one button click
* Table layout improves usability for task forms

---

# Level 6: Customizing Inline FormSets

* Add validation and customization to inline formsets

```python
from django.forms import BaseInlineFormSet

class TaskBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        """Validate the formset as a whole."""
        super().clean()
        
        # Count completed tasks
        completed_count = 0
        for form in self.forms:
            if not form.is_valid():
                continue
                
            if form.cleaned_data.get('DELETE'):
                continue
                
            if form.cleaned_data.get('status') == 'COMPLETED':
                completed_count += 1
        
        # Validation example: at least one task must be completed
        if completed_count == 0 and self.instance.pk:  # Only for existing projects
            raise forms.ValidationError(
                "At least one task must be marked as completed"
            )

# Use the custom formset class
TaskInlineFormSet = inlineformset_factory(
    Project,
    Task,
    formset=TaskBaseInlineFormSet,
    fields=('name', 'status', 'due_date'),
    extra=2,
    can_delete=True
)
```

* `BaseInlineFormSet` allows custom validation for the entire formset
* Can check relationships between different forms
* `self.instance` gives access to the parent Project

---

# Level 6: Custom Form Widgets

* Improve the user experience with custom widgets

```python
class TaskInlineForm(forms.ModelForm):
    """Custom form for Task model in inline context."""
    class Meta:
        model = Task
        fields = ('name', 'status', 'due_date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'task-name-field',
                'placeholder': 'Enter task name'
            }),
            'status': forms.Select(attrs={
                'class': 'task-status-field'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'task-date-field'
            }),
        }

# Use the custom form in the formset
TaskInlineFormSet = inlineformset_factory(
    Project,
    Task,
    form=TaskInlineForm,
    formset=TaskBaseInlineFormSet,
    extra=2,
    can_delete=True
)
```

* Creating a custom ModelForm for the inline formset
* Using HTML5 date input with `type='date'`
* Adding CSS classes for styling

---
# Conclusion: Mastering Django Forms

* We've journeyed from basic ModelForms to advanced dynamic FormSets
* Django's form system provides powerful tools for your applications:
  * Basic ModelForms automate CRUD operations on your models
  * Custom validation ensures data integrity
  * Inline FormSets handle parent-child relationships elegantly
  * Dynamic forms adapt to user choices

* Forms are the bridge between your models and your users:
  * Convert complex database structures into intuitive interfaces
  * Validate input before it reaches your database
  * Handle relationships between Projects, Tasks, and TeamMembers