---
title: Creating a Project Base
created: 2022-02-22
tags:
  - beginners
  - python
  - web development
  - django
  - htm
  - css
  - javascript
  - htmx
---

{~ hero layout="text_left_image_right" image_src="https://ucarecdn.com/19205348-9397-400e-89c5-053a6da9adeb/-/resize/1050/" image_alt="Laptop displaying code with a cup of coffee" text_bg_color="white-50" text_color="neutral-800" ~}

## Launch Your Web Development Journey: Django & HTMX

Whether you're taking your first steps in web development or looking to structure your Python web projects more effectively, you're in the right place!

{~~}

Welcome, aspiring web developer! This course is designed to be your launchpad into the exciting world of creating dynamic, modern web applications. We'll guide you step-by-step as we construct a solid project base using the powerful Python framework **Django**, explore the innovative **HTMX** library for crafting interactive user interfaces with surprising simplicity, and master the essential building blocks of the web: **HTML, CSS, and JavaScript**.

Our philosophy is that learning web development should be accessible and engaging. We've tailored this journey to be as beginner-friendly as possible, breaking down complex concepts into manageable pieces. So, whether you're completely new to programming or you already have some Python basics under your belt and are eager to apply them to the web, you'll gain the practical skills and confidence to bring your web ideas to life. We'll focus on understanding *why* things work, not just *how*, ensuring you build a strong foundation for future learning and development.

{~ alert type="info" ~}
### Prerequisites

- Python installed (3.10+ recommended, <3.12 due to potential Django 5.1 compatibility nuances with very latest Python versions at time of writing, always check Django docs for specific version pairings)
- Basic understanding of programming concepts (variables, loops, functions, etc.)
- A command-line terminal or shell.
- Enthusiasm to learn and build!
{~~}

### What You'll Learn

#### Django 5.1

- Effortless installation using pip.
- A comprehensive walkthrough of setting up a new Django project from scratch.
- The fundamentals of back-end development: models, views, templates, and URL routing.
- How to leverage Django's "batteries-included" features like the admin panel.

#### HTMX 2.0

- Simple integration into your Django project.
- How to create Hypermedia-Driven Applications, reducing the need for complex JavaScript.
- Utilizing the `django-htmx` library for enhanced Django-specific HTMX functionality.

#### HTML/CSS/JavaScript

- This course **will cover** the essential HTML structure, CSS styling, and JavaScript interactions needed.
- Solidify your understanding of these core front-end technologies.
- We aim for minimal custom JavaScript, demonstrating how HTMX can simplify client-side interactivity.

---

## What is Django?

> "The web framework for the perfectionist on a deadline."

Django is a **high-level, open-source** web framework that uses Python to solve common web development problems. Each component of Django is **loosely coupled**, meaning they can be managed independently.

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│   Browser   │◄────►│     URL     │─────►│    View     │
│   Request   │      │  Resolver   │      │   (Logic)   │
│             │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
                                                │
                                                │
                                                ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│   Browser   │◄────►│  Template   │◄─────│    Model    │
│   Display   │      │   (HTML)    │      │   (Data)    │
│             │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
```

{~ card title='🔋"Batteries Included": Django has Superpowers!' footer='These built-in features save you tons of development time.' ~}

Django isn't just a basic toolkit; it comes packed with many useful pre-built features right out of the box. This "batteries included" philosophy means you spend less time reinventing the wheel and more time building unique features for your application. Key batteries include:

* **Admin Interface:** An automatic, production-ready interface for managing your site's content.
* **Authentication System:** Handles user accounts, groups, permissions, and cookie-based user sessions.
* **Forms Framework:** A powerful system for creating HTML forms, validating data, and processing submissions.
* **ORM (Object-Relational Mapper):** Lets you interact with your database using Python code instead of SQL (Database Abstraction).
* **Testing Framework:** Tools to write and run tests for your application, ensuring reliability.
{~~}

{~ alert type="info" ~}

**How Django Handles a Web Request** 🌐

Understanding the flow of a request in Django is key to grasping how it works. Here's a typical sequence, inspired by insights from resources like [dothedev.com](https://www.dothedev.com/blog/what-is-django-used-for/):

1. **User Request:** It all starts when a user interacts with their browser, usually by typing a URL or clicking a link. The browser sends this request to your Django application.
2. **URL Resolving:** Django receives the URL and consults its "URLconf" (URL configuration) to find a matching pattern. This is like a traffic controller directing the request to the right place.
3. **View Logic:** Once a URL pattern matches, Django calls the associated "view" function (or class-based view). This is where your main application logic lives. The view processes the request, interacts with data models if needed, and decides what response to send back.
4. **Model Interaction (Data Handling):** If the view needs to fetch or save data (like user information or blog posts), it interacts with Django's "models." Models define the structure of your application's data and provide an interface (the ORM) to the database.
5. **Template Rendering (Generating HTML):** After the view has processed the request and gathered any necessary data, it typically loads a "template." The template is an HTML file (often with special Django template tags) that defines the structure of the webpage. The view passes data to the template, which then renders the final HTML to be sent back to the user's browser.
6. **HTTP Response:** Finally, Django bundles up the rendered HTML (or other content type) into an HTTP response, which is sent back to the user's browser to be displayed.
{~~}

---

## Creating your Project

{~ label_seperator color="primary" ~}
**Step 1:** Create and activate a Virtual Environment
{~~}

```sh
python -m venv venv
```

Creates a Virtual Environment called `venv`

To activate the venv on **windows**:

```sh
venv\Scripts\activete
```

To activate the venv on **Linux**:

```sh
source venv/bin/activate
```

{~ label_seperator color="primary" ~}
**Step 2:** Install Django to your Virtual Environment
{~~}

```sh
python -m pip install Django
```

{~ label_seperator color="primary" ~}
**Step 3:** Create your first Project
{~~}

```sh
django-admin startproject _core .
```

`_core` is the name of the folder to create
`.` is the folder to put it in

---

## Understand the Folder Structure

### manage.py
Very important file used for **console commands**. Your terminal will access this to do things like create apps, super users, migrate databases, etc.
### core/urls.py
The base or “core” of URL routing. Empty by default except for the built-in admin panel routes. We will use **include()** to separate urls for different apps.
### core/settings.py
A file you will be coming back to often. Contains **important configuration** for things like installed_apps, security features, plugins, etc.

---
## Creating Your First App!

> A Django Project can have many Apps

{~ label_seperator color="primary" ~}
**Step 1:** Type the console command:
{~~}

```sh
python manage.py startapp A_base
```

I prefer to put the A_ for alphabetical ordering. A stands for App. This keeps our folders neat.

### models.py

Defines your database structure using Python classes - each class represents a database table and defines what data you want to store and how it relates to other data. (Blog Posts, User Comments, Profiles, etc.)

### views.py

Functions or classes that receive web requests and return web responses - this is where you put your main logic for handling what users see and do on your website. Like gears turning behind the scenes.

### admin.py

Configures how your models appear in Django's built-in admin interface - it's where you register models to make them manageable through Django's automatic admin dashboard. Django’s admin is very powerful!

---

## Creating your First App! - 2

> Time to create some files

{~ label_seperator color="primary" ~}
**Step 2:** Create A_base/urls.py:
{~~}

This is like the “table of contents” for your app. It maps URLS (web addresses) to the appropriate views. We will link this app’s urls to _core/urls.py later, but for now we can keep this file empty.

{~ label_seperator color="primary" ~}
**Step 3:** Create A_base/templates/A_base/base.html:
This is going to be the front-end file that the user sees on your site.
{~~}

This will be like a blueprint that all other pages inherit from. It will contain the boilerplate HTML setup, any necessary scripts/styles, navigation bars, and many other things that we don’t want to type over and over again.

Why this structure?

1. Django looks in all apps' for a folder named ‘templates’
2. The app-named folder (A_base) prevents template name conflicts - Without it, `base.html` in multiple apps would clash - With it, Django can find `A_base/base.html` specifically

---

## Creating your First App! - 3

> Get familiar with your settings, you'll come back to it often

{~ label_seperator color="primary" ~}
**Step 4:** update INSTALLED_APPS in core/settings.py
This is how your project knows that your app exists. Otherwise, it won’t find the new files.
{~~}

```python
# _core/settings.py
INSTALLED_APPS = [
    # other apps
    'A_base',
]
```

---

## A_base/templates/A_base/base.html

> Let's get to coding!

{~ label_seperator color="primary" ~}
**Step 1 - Boiler plate base.html:**
{~~}

```html
<!DOCTYPE html>
<html lang="en">
<!-- must be wrapped in a html tag -->
</html>
```

{~ label_seperator color="primary" ~}
**Step 2 - Head:**
{~~}

```html
{% verbatim %}
<html lang="en">
<head>
    <!-- Character encoding for Unicode/emoji support -->
    <meta charset="UTF-8" />
    <!-- Makes website mobile-friendly -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <!-- The title that appears in browser tab -->
    <title>{% block title %}My Website{% endblock %}</title>
</head>
{% endverbatim %}
```

This is some important boilerplate html code that you'll likely be writing at least once for every project on the web.

The file must start with `<!DOCTYPE html>`, and everything must be wrapped in the `<html></html>` tags.

The `<head>` contains important meta data, like the screen size, fonts, and title.

We will return to this `<head>` section often to insert things like style, scripts, fonts, and more.

`% block title %My Website% endblock %` represents an interchangeable title.

---

## A_base/templates/A_base/base.html - 2

> The Body is the most important part!

{~ label_seperator color="primary" ~}
**Step 3 - Create the body:**
{~~}

This very simple body will house the main content of our website.

`<a href="#">` represents a link, the `#` means it's empty (for now).

`% block content % % endblock %` represents an interchangeable part. We can insert new html files here, while still keeping this html structure.

```html
{% verbatim %}
</head>
<body>
    <!-- Navigation bar -->
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
        </ul>
    </nav>
    <!-- Main content area -->
    <main>
        {% block content %}
        <!-- Other pages will put their content here -->
        My Content Here {% endblock %}
    </main>
    <!-- Footer area -->
    <footer>
        <p>&copy; 2025 My Website</p>
    </footer>
</body>
</html>
{% endverbatim %}
```

---

## A_base/views.py

This is where the magic starts!

**Create the basic View Function:**

```python
from django.shortcuts import render

def base_view(request):
    context = {}
    template = "A_base/base.html"
    return render(request, template, context)
```

**render:**  
A **Django function** that combines an **HTML template** with your **Python data** and returns it as a **webpage** to the user. This is one of the most common functions to import and use in views.

**context:**  
A **dictionary** that passes **data** from your **Python view** to your **HTML template** - currently empty ({}), but could contain things like `{'username': 'John'}` to display in the template.

**template:**  
The path to your **HTML** file that Django will use to create the **webpage** - in this case the "A_base/base.html" file that we created earlier.

**request:**  
Contains all the **information** about the current webpage request - like who's asking for the page, what method they're using (**GET/POST**), and any data they're sending.

---

## Map the URLS

Allow access to the view

{~ label_seperator color="primary" ~}
**Step 1**  
Update A_base/urls.py:
{~~}

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name="base"),
]
```

{~ label_seperator color="primary" ~}
**Step 2**  
Add to _core/urls.py:
{~~}

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('A_base.urls')),
]
```

**path:**  
Connects a URL pattern (like 'admin/' or '') to the code that should handle it - think of it like creating a road that leads to a specific destination.

**include:**  
Lets you plug in URLs from your apps - instead of listing all URLs in one file, you can split them into separate apps.

---

## Start The Server

Now you can visit your site!

**Type the Console Command:**
```
python manage.py runserver
```

```
February 22, 2025 - 07:04:39
Django version 5.1.6, using settings '_core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Enter this URL in your web browser:**

`127.0.0.1:8000` or `localhost:8000`

Because the URL path we created is empty (`""`), this will lead us to our `base_view`.

If the path was `"test"`, we would need to visit `localhost:8000/test`

---

## The Django Architecture - Requests 🌐

Understanding how Django processes an HTTP request from a user's browser to delivering a webpage is fundamental to web development with the framework. This well-defined cycle involves several key stages.

{~ card title="Understanding Django's Request-Response Cycle" footer="Key steps from initial browser request to final page display." ~}
Here’s a step-by-step breakdown of how Django typically handles an incoming HTTP request and crafts an appropriate response:

1. **Initial Request (Browser to Django):**
    The process begins when a **Web Browser**, acting on behalf of a user, requests a specific page via its URL. This HTTP request is first received by a web server (like Nginx or Apache if in production, or Django's development server), which then passes it to the Django framework for processing.

2. **URL Resolution (Pattern Matching):**
    Django examines the requested URL and compares it against its list of configured **URL patterns**. These patterns are typically defined in `urls.py` files within your project and apps. Django proceeds with the first pattern in the list that successfully matches the requested URL.

3. **View Execution (Processing Logic):**
    Upon finding a matching URL pattern, Django invokes the corresponding **view** function or class-based view. The view contains the core application logic required to handle the request. This might involve accessing data, performing calculations, or interacting with other services.

4. **Model Interaction (Data Management):**
    If the **view** needs to access or manipulate persistent data (e.g., read from or write to a database), it interacts with Django's **data models**. Models define the structure, relationships, and integrity of the application's data. This interaction is usually facilitated by Django's Object-Relational Mapper (ORM), which allows you to work with database records as Python objects.

5. **Template Rendering (Generating Output):**
    After the view has processed the request and gathered any necessary data (often from the models or through its own logic), it typically renders a **template**. Templates (usually HTML files, but they can be other formats like XML or JSON) define the structure and presentation of the output. The view passes a "context" (a dictionary of data) to the template, which then uses this data to generate the final content (e.g., an HTML page).

6. **HTTP Response (Sending to Browser):**
    Finally, Django packages the rendered content (e.g., the HTML page) into an **HTTP response**. This response, along with appropriate HTTP headers and status codes, is sent back to the user's **Web Browser**, which then interprets and displays the content.
{~~}

---

**HTTP (Hypertext Transfer Protocol)** is how browsers communicate with servers.

The most common request methods are `GET` and `POST`.

`GET` requests ask for resources, like when you visit a webpage.

`POST` requests submit data, like when you fill out a form.

The server processes these requests and sends back an **HTTP response** with a **status code** (`200` for success, `404` for not found, etc.) and the requested data.

This data could be HTML for a webpage, JSON for an API, files for downloads, or other content types.

---

{~ alert type="success" ~}

**Don't worry** - with this course, we're breaking down these concepts into **manageable steps**!

Django's organized architecture actually makes web development more approachable once you understand the pattern. We'll work through each piece together, and you'll be building websites before you know it.
{~~}
