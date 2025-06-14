---
title: Models and Admin Interface
created: 2022-02-25
tags:
  - beginners
  - python
  - web development
  - django
  - html
  - css
  - javascript
---

## Create a Model

Models are a source of information about the behaviors of your data.
Each model maps to a single database table, where each attribute of the class represents a database field.
### A_base/models.py:
```python
from django.db import models

# All Models inherit from django.db.models.Model
class TeamMember(models.Model):
    # CharField - Text with a maximum length
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    # TextField - Text with no maximum length
    bio = models.TextField()
    # DateField - Stores a date
    join_date = models.DateField(auto_now_add=True)

    # __str__ - How to display the object in the admin
    def __str__(self):
        return f"{self.name} - {self.role}"

    # Meta - Other information about the model
    class Meta:
        ordering = ['join_date']
```

---
## Migrate to the Database

Now that we have the `models.py` code, we need to create the database table.
Django comes with a migration system that tracks the changes made to models and inserts them into the database.
### Step 1 - Make Migrations:
```
python manage.py makemigrations
```
### Step 2 - Migrate:
```
python manage.py migrate
```

All of the apps from INSTALLED_APPS that we saw in _core/settings.py, including our A_base app will migrate all of their database tables.

Django is Database Agnostic, but it uses sqlite3 by default, automatically creating a db.sqlite3 file in your project's directory.

---
## Introduction to Django Admin
### Unlock Django's Built-In Superpowers: The Admin Interface

### What is the Admin UI?
○   A pre-built dashboard for managing data (CRUD operations).
○   Automatically generated from your models.
○   Only accessible to users with `staff` or `superuser` privileges.
### Why Use It?
○   Rapidly test database entries during development.
○   Avoid building a custom admin panel from scratch.
○   Manage users, groups, permissions, and app data.
### Key Features
○   Search, filter, and sort records.
○   Bulk actions (delete, update).
○   Audit logs (if enabled).

```python
from .models import TeamMember
# Simplest way to register a model
admin.site.register(TeamMember)
```

```
python manage.py createsuperuser
```

Minimal coding needed for basic use—Django does the heavy lifting!

---
## Customizing the Admin
### Tailor the Admin to Your Needs

### Custom Admin Classes
• Subclass `admin.ModelAdmin` to override defaults.

### Common Customizations
• `list_display`: Show specific fields
• `prepopulated_fields`: Auto-generate slugs.
• `readonly_fields`: Prevent edits (e.g., `join_date`).

```python
from django.contrib import admin
from .models import TeamMember

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "join_date")  # Columns in list view
    search_fields = ("name", "role")  # Add a search bar
    list_filter = ("join_date",)  # Filter by date
    readonly_fields = ("join_date",)  # Make join_date read-only

admin.site.register(TeamMember, TeamMemberAdmin)
```

## Create an 'about' page

Create a new function in A_base/views.py:

```python
from .models import TeamMember

def about_view(request):
    team_members = TeamMember.objects.all()
    context = {'team_members': team_members}
    template = "A_base/about.html"
    return render(
        request,
        template,
        context
    )
```

### TeamMember.objects.all()
Retrieves a list of every TeamMember instance in your database.

Create a new url path in A_base/urls.py:

```python
urlpatterns = [
    path("", views.base_view, name="base"),
    path("about/", views.about_view, name="about"),
]
```

---
## New Template to show Team Members

A_base/templates/A_base/about.html:

```django
{% verbatim %}
{% extends "A_base/base.html" %}

{% block content %}
<h1>About</h1>
<p>This is the about page</p>
<h2>Team Members</h2>
{% for member in team_members %}
    <strong>{{ member.name }}</strong>
    <span style="opacity: 0.5;">{{ member.role }}</span>
    <p style="text-indent: 16px;">{{ member.bio }}</p>
{% endfor %}
{% endblock %}
{% endverbatim %}
```

### % extends "A_base/base.html" %
The base html file this extends from. The % block content %} part of this template will alter the same-named block of the extended base template.

### % for member in team_members %
Accesses the 'team_members' variable from the view's context. The for loop will create the paragraph & strong element for each member in this list.

### { member.name/.role/.bio }
Accesses and shows the 'name', 'role', and 'bio' fields of each member in the 'team_members' list.

### % endfor % and % endblock %
Be sure to end your for loops and blocks, or else you will get an error when you try to load this page.

### style="opacity: 0.5;" and "text-indent: 16px;"
A little taste of CSS. Take note of the syntax, the variable name followed by a colon(:) then the value then a semicolon (;)

---
## Preview of our (mostly unstyled) website

Update the nav links in A_base/base.html

```html
% verbatim %}
<nav>
    <ul>
        <li><a href="% url 'base' %}">Home</a></li>
        <li><a href="% url 'about' %}">About</a></li>
    </ul>
</nav>
% endverbatim %}
```

### % url 'base' % and % url 'about' %

The 'url' tag will search for the urlpatterns we have defined in A_base/urls.py by their 'name' attribute:

```python
urlpatterns = [
    path("", views.base_view, name="base"),
    path("about/", views.about_view, name="about"),
]
```

Notice how the **Nav** and the **Footer** are still there, even though it's a new html file? That's because A_base/about.html has **extended** from A_base/base.html!

---
## Create a New App

Apps are **Modular.** Lets create a new app for new models.

Type this into your terminal:
```
python manage.py startapp A_projects
```

Remember to add to `_core/settings.py`
```python
#_core/settings.py
INSTALLED_APPS = [
	"A_projects",
]
```

Update `_core/urls.py`
```python
#_core/urls.py
urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("A_base.urls")),
	path("projects/", include("A_projects.urls")),
]
```

---
## Model Relationships
### Team Members & Projects: Many-to-Many Relationships

Add a new model to A_projects/models.py
```python
from django.template.defaultfilters import slugify

from A_base.models import TeamMember

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    description = models.TextField()
    # ManyToManyField - Many objects can be related to one another
    members = models.ManyToManyField(
        TeamMember,
        related_name='projects', # used to access related objects
        blank=True # Allows empty projects
    )
    start_date = models.DateField(auto_now_add=True)
    # SlugField - Used to create a URL
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    # this function is called when the object is saved
    def save(self, *args, **kwargs):
        # ensures that there is a slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['start_date']
```

### def save(self, args, kwargs):
This function will be called whenever an instance of this model gets saves to a database. In this case, we ensure that the instance has a slug based on the name.

### super().save(args, kwargs)
super() accesses the class that this extends from (models.Model), then we call this parent class' save function AFTER we do our custom save logic. This ensures the model is properly saved.

### related_name='projects'
Allows team_member.projects.all() to get all projects for a member.

### SlugField and slugify
A slug is a string that is URL-friendly, instead of "This is my Title", slugify transforms it to "this-is-my-title"

---
## Admin Integration
### Managing Relationships in Django Admin

Update A_projects/admin.py
```python
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date")
    filter_horizontal = ("members",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    readonly_fields = ("start_date",)

admin.site.register(Project, ProjectAdmin)
```

### prepopulated_fields
makes a slug auto-generate as you type a name

### filter_horizontal
makes the creation UI for handling relationships much better:

![Admin interface showing horizontal filter with two columns - Available members and Chosen members with arrow controls between them]

Hold down "Control", or "Command" on a Mac, to select more than one.

---
## Querying Relationships

Update A_base/templates/A_base/about.html inside the members loop, below the bio
```django
% verbatim %}
<p style="text-indent: 16px;">{{ member.bio }}</p>
% if member.projects.all.count == 1 %}
   <p>{{ member.projects.all.count }} project</p>
% elif member.projects.all.count > 1 %}
   <p>{{ member.projects.all.count }} projects</p>
% else %}
   <p>No projects</p>
% endif %}

% for project in member.projects.all %}
   <p>
      <a href="#">{{ project.name }}</a>
   </p>
% endfor %}
% endverbatim %}
```

### % if % and % elif % and % else %
Just like Python, you can use comparison operators like == or > to check conditions!

### .projects.all.count
This returns the amount of all the member's projects (remember related_name)

---
## Slug-Based Detail View
### Creating Friendly URLs with Slugs

Update A_projects/urls.py
```python
from django.urls import path

from . import views

urlpatterns = [
    path(
        "<slug:slug>/",
        views.project_detail_view,
        name="project_detail"
    ),
]
```

### URL Parameters (<slug:slug>):
Matches URL patterns like /projects/my-awesome-project/

slug type ensures URL-safe format (auto-created via slugify)

Create the project_detail_view at A_base/views.py
```python
from django.shortcuts import render, get_object_or_404

from .models import Project

def project_detail_view(request, slug):
    project = get_object_or_404(
        Project,
        slug=slug
    )
    context = {'project': project}
    template = "A_projects/project_detail.html"
    return render(
        request,
        template,
        context
    )
```

This view takes the slug from the URL parameter. It then uses this slug to find the corresponding project.

If that project is not found, get_object_or_404 will automatically return an error page.

---
## Project Detail Template
### Building the Project Page

Create A_base/templates/A_base/project_detail.html
```django
% verbatim %}
% extends "A_base/base.html" %}
% endverbatim %}

% verbatim %}
% block content %}
<h1>{{ project.name }}</h1>
<p>{{ project.description }}</p>
<h2>Members</h2>
% for member in project.members.all %}
    <strong>{{ member.name }}</strong>
    <span style="opacity: 0.5;">{{ member.role }}</span>
    <p style="text-indent: 16px;">{{ member.bio }}</p>
% endfor %}
% endblock %}
% endverbatim %}
```

Update the url in the projects for loop on about.html
```django
% verbatim %}
% for project in member.projects.all %}
<p>
    <a href="% url 'project_detail' project.slug %}">{{ project.name }}</a>
</p>
% endfor %}
% endverbatim %}
```

This will automatically populate the href with the correct project's full URL based on the slug

---
## Splitting up the templates
### Notice we had to write the member info twice? Let's fix that!
A_projects/project_detail.html
A new folder in your templates called "snippets"
Create templates/A_base/snippets/member_info.html:
```html
% verbatim %}
<strong>{{ member.name }}</strong>
<span style="opacity: 0.5;">{{ member.role }}</span>
<p style="text-indent: 16px;">{{ member.bio }}</p>
% endverbatim %}
```

Now instead of rewriting this every time we want to show member info, we can use the % include % tag

A_base/about.html:
```django
% verbatim %}
% for member in team_members %}
    % include "A_base/snippets/member_info.html" %}
% endfor %}
% endverbatim %}
```

A_projects/project_detail.html:
```django
% verbatim %}
% for member in project.members.all %}
    % include "A_base/snippets/member_info.html" %}
% endfor %}
% endverbatim %}
```

**Splitting your templates** up like this is a good habit to get into.

Not only do you no longer have to rewrite the same code, if you ever want to edit how the members are displayed, you now only have to edit one single file rather than two.

---
## Create a list view
### A view to list all the projects

Update A_projects/urls.py
```python
urlpatterns = [
    path("", views.project_list_view, name="project_list"),
    path(
        "projects/<slug:slug>/",
        views.project_detail_view,
        name="project_detail"
    ),
]
```

In A_projects/views.py, create a project_list_view
```python
def project_list_view(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    template = "A_projects/project_list.html"
    return render(
        request,
        template,
        context
    )
```

### Hopefully you are noticing a pattern

First, we create the view/url

Next, we will create the template

---
## Create a list view - 2
### A view to list all the projects

Create A_base/templates/A_base/project_list.html
```django
% verbatim %}
% extends "A_base/base.html" %}

% block content %}
<h1>Projects</h1>
% for project in projects %}
    <h2><a href="% url 'project_detail' project.slug %}">
        {{ project.name }}
    </a></h2>
    <p>{{ project.start_date }}</p>
    <p>{{ project.members.all.count }} members</p>
% endfor %}
% endblock %}
% endverbatim %}
```

Add a new link to the nav bar in base.html
```html
<nav>
    <ul>
        <li><a href="% url 'base' %}">Home</a></li>
        <li><a href="% url 'about' %}">About</a></li>
        <li><a href="% url 'project_list' %}">Projects</a></li>
    </ul>
</nav>
```

Now our navigation includes links to all main sections of our site.

---
## Model Relationships: ForeignKey
### Tasks & Projects: One-to-Many Relationships

Add a new model to A_base/models.py
```python
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    name = models.CharField(max_length=100, default="New Task")
    description = models.TextField(blank=True)
    # ForeignKey - Creates a One-to-Many relationship
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,  # If project is deleted, delete related tasks
        related_name='tasks'       # Access via project.tasks.all()
    )
    # CharField with choices
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,    # Limits input to these choices
        default='PENDING'
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.name} - {self.project.name}"
```

### Choices vs. ForeignKey:
- **Choices**: Good for predefined options that won't change often (statuses, priorities)
- **ForeignKey**: Good for relationships to other database tables that may grow

After creating this model, run:
```
python manage.py makemigrations
python manage.py migrate
```

## Model Relationships: OneToOneField
### Extending Django's User Model

Modify the TeamMember model in A_base/models.py to link with Django's built-in User model:

```python
from django.db import models
from django.contrib.auth import get_user_model

# Get the currently active User model
User = get_user_model()

class TeamMember(models.Model):
    # Link to Django's User model using best practice
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='team_profile',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['join_date']
```

### OneToOneField vs. ForeignKey
- **OneToOneField**: Exactly one related object in each direction
- **ForeignKey**: Many records can point to the same related object

After modifying the model, run:
```
python manage.py makemigrations
python manage.py migrate
```

---
## Enhanced Admin for OneToOne Relationship
### Editing the TeamMember A_Base/Admin Interface

```python
from django.contrib import admin

from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'join_date', 'linked_user')
    list_filter = ('role', 'join_date')
    search_fields = ('name', 'role', 'user__username')

    # Custom field to display in list view
    def linked_user(self, obj):
        if obj.user:
            return obj.user.username
        return '(No user linked)'
    linked_user.short_description = 'User Account'

    # Customize fields shown during editing
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'bio')
        }),
        ('User Account', {
            'fields': ('user',),
            'description': 'Link this team member to a Django user account'
        }),
    )

    # Add autocomplete for User field
    autocomplete_fields = ['user']

```

1. **Decorator Registration** (`@admin.register(TeamMember)`):
   - Alternative to `admin.site.register()` that allows cleaner code
   - Registers the model and its admin class in one step

2. **Custom Methods for Display** (`linked_user`):
   - Create methods inside admin classes to format or process data
   - Use `short_description` to set column header text
   - Ideal for derived fields or formatting complex data

3. **Related Lookups** (`search_fields = ('user__username',)`):
   - The double-underscore syntax accesses fields in related models
   - Enable searching across relationships without extra code

4. **Fieldsets for Organized Forms**:
   - Group related fields under logical headings
   - Add descriptions to provide context for editors
   - Create a more structured editing experience

5. **Autocomplete for Better UX** (`autocomplete_fields`):
   - Converts select fields to searchable dropdowns
   - Critical for models with many possible relations
   - Prevents overwhelming admins with too many choices

---
## Admin Inline Models
### Edit Related Tasks Within Projects

Update A_projects/admin.py to add inline task editing to projects:

```python
from django.contrib import admin
from .models import Project, Task

# Create an inline admin model for tasks
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1  # How many empty forms to show
    fields = ('name', 'status', 'due_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date")
    filter_horizontal = ("members",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    readonly_fields = ("start_date",)

    # Add the inline to the Project admin
    inlines = [TaskInline]

# No need to register Task separately if we only want to edit it
# within the context of a Project
```

1. **TabularInline vs StackedInline**:
   - `TabularInline`: Compact, table-like format (good for many items)
   - `StackedInline`: Each related object gets a full form layout (more space)

2. **Parent-Child Editing**:
   - The foreign key relationship is automatically handled
   - Tasks are always associated with the correct project

3. **No Need for Separate Registration**:
   - You don't need to register Task with `admin.site.register()`
   - This prevents cluttering the admin index with models better edited inline
