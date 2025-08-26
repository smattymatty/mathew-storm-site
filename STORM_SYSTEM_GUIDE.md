Storm System - Agent Instructions for Django Spellbook Projects

  🎯 Purpose

  This guide is for AI agents building Django websites using the Storm
  System animation library with Django Spellbook's design system. The Storm
   System allows you to create professional, animated websites using only 
  HTML attributes - no JavaScript or CSS knowledge required.

  ⚡ Core Principle

  You should NEVER write custom JavaScript or CSS for animations. The Storm
   System handles everything through HTML data attributes. Your job is to
  add the right attributes to Django templates using Spellbook's sb-
  classes.

  📋 Prerequisites

  Ensure the Django project has Storm System installed in the base
  template:

  {# base.html #}
  {% load static %}
  {% load spellbook_tags %}
  <!DOCTYPE html>
  <html>
  <head>
      {% spellbook_styles %}
      <!-- Other head content -->
  </head>
  <body>
      {% block content %}{% endblock %}

      <!-- Storm System (place before closing body) -->
      <script type="module">
          import StormAnimations from '{% static "js/storm-animations.mjs"
  %}';
          import StormEvents from '{% static "js/storm-events.mjs" %}';
          // Auto-initializes - no configuration needed
      </script>
  </body>
  </html>

  🎨 HTML-Only Animation Guide with Spellbook Classes

  Basic Entrance Animations

  Add these attributes to any HTML element with Spellbook classes:

  {# Simple fade in with Spellbook typography #}
  <h1 class="sb-text-4xl sb-font-bold" data-storm="fade-in">{{ page.title
  }}</h1>

  {# Slide animations with delays and Spellbook spacing #}
  <div class="sb-p-4 sb-bg-surface" data-storm="slide-up" 
  data-storm-delay="200">
      {{ page.description }}
  </div>

  {# Multiple elements with staggered timing #}
  {% for feature in features %}
      <div class="sb-card sb-p-6" data-storm="slide-right" 
  data-storm-delay="{{ forloop.counter0|multiply:100 }}">
          <h3 class="sb-text-2xl sb-mb-2">{{ feature.title }}</h3>
          <p class="sb-text-secondary">{{ feature.description }}</p>
      </div>
  {% endfor %}

  Available Animation Names

  Entrance Effects (use on page load)

  - fade-in - Fades in from invisible
  - slide-up - Slides up from below
  - slide-down - Slides down from above
  - slide-left - Slides in from right
  - slide-right - Slides in from left
  - zoom-in - Zooms in from small
  - scale-up - Scales up from center
  - bounce-in - Bounces in
  - blur-in - Blurs in from fuzzy
  - rotate-in - Rotates in

  Hero Section Animations

  - hero-title - Special animation for main titles
  - hero-subtitle - For subtitles
  - hero-description - For hero descriptions

  Interactive Hover Effects with Spellbook Buttons

  {# Spellbook buttons that lift on hover #}
  <button data-storm="hover-lift" class="sb-btn sb-btn-primary">
      {{ button.text }}
  </button>

  {# Secondary button with hover effect #}
  <button data-storm="hover-scale" class="sb-btn sb-btn-secondary">
      {{ button.text }}
  </button>

  {# Accent button with glow #}
  <button data-storm="hover-glow" class="sb-btn sb-btn-accent">
      {{ button.text }}
  </button>

  {# Cards with Spellbook styling #}
  <div data-storm="hover-scale" class="sb-card sb-shadow-lg sb-p-6">
      <img src="{{ card.image.url }}" alt="{{ card.title }}" 
  class="sb-rounded-lg sb-mb-4">
      <h3 class="sb-text-xl sb-font-semibold">{{ card.title }}</h3>
      <p class="sb-text-secondary sb-mt-2">{{ card.description }}</p>
  </div>

  Click Animations with Spellbook Components

  {# Spellbook button that bounces when clicked #}
  <button data-storm-click="bounce" class="sb-btn sb-btn-primary 
  sb-w-full">
      Submit Form
  </button>

  {# Error message with Spellbook alert styling #}
  <div data-storm-click="shake" class="sb-alert sb-alert-error">
      Click to dismiss
  </div>

  {# Special offer with Spellbook badge #}
  <div data-storm-click="sparkles" class="sb-badge sb-badge-accent">
      ✨ Special Offer ✨
  </div>

  Combining Effects with Spellbook Layout

  {# Entrance + hover effect with Spellbook grid #}
  <div class="sb-grid sb-grid-cols-3 sb-gap-4">
      <div data-storm="fade-in" data-storm-hover="scale" 
  data-storm-delay="300" 
           class="sb-card sb-p-4">
          {{ content }}
      </div>
  </div>

  {# Multiple entrance animations with Spellbook typography #}
  <h1 data-storm="fade-in slide-up" data-storm-delay="200" 
      class="sb-text-5xl sb-font-bold sb-text-primary">
      {{ hero.title }}
  </h1>

  📝 Django Template Patterns with Spellbook Classes

  Hero Section Pattern

  {# hero_section.html #}
  <section class="sb-hero sb-py-20 sb-px-4 sb-bg-gradient">
      <div class="sb-container sb-mx-auto">
          <h1 data-storm="hero-title" class="sb-text-6xl sb-font-bold 
  sb-text-center">
              {{ hero.title }}
          </h1>
          <h2 data-storm="hero-subtitle" data-storm-delay="300" 
              class="sb-text-2xl sb-text-secondary sb-text-center sb-mt-4">
              {{ hero.subtitle }}
          </h2>
          <p data-storm="hero-description" data-storm-delay="600"
             class="sb-text-lg sb-text-center sb-max-w-2xl sb-mx-auto 
  sb-mt-6">
              {{ hero.description }}
          </p>
          <div class="sb-flex sb-justify-center sb-mt-8">
              <button data-storm="fade-in" data-storm-delay="900" 
  data-storm-hover="lift"
                      class="sb-btn sb-btn-primary sb-btn-lg">
                  {{ hero.cta_text }}
              </button>
          </div>
      </div>
  </section>

  Feature Cards Pattern

  {# features_section.html #}
  <section class="sb-section sb-py-16">
      <div class="sb-container sb-mx-auto">
          <h2 data-storm="fade-in" class="sb-text-4xl sb-font-bold 
  sb-text-center sb-mb-12">
              Our Features
          </h2>
          <div class="sb-grid sb-grid-cols-1 sb-md:grid-cols-3 sb-gap-6">
              {% for feature in features %}
                  <div data-storm="slide-up" 
                       data-storm-delay="{{ forloop.counter0|multiply:200
  }}"
                       data-storm-hover="scale"
                       class="sb-card sb-shadow-md sb-p-6">
                      <i class="sb-icon sb-icon-{{ feature.icon }} 
  sb-text-4xl sb-text-primary sb-mb-4" 
                         data-storm-click="bounce"></i>
                      <h3 class="sb-text-xl sb-font-semibold sb-mb-2">{{
  feature.title }}</h3>
                      <p class="sb-text-secondary">{{ feature.description
  }}</p>
                  </div>
              {% endfor %}
          </div>
      </div>
  </section>

  Testimonials Pattern

  {# testimonials.html #}
  <section class="sb-section sb-bg-subtle sb-py-16">
      <div class="sb-container sb-mx-auto">
          <div class="sb-grid sb-grid-cols-1 sb-md:grid-cols-2 sb-gap-8">
              {% for testimonial in testimonials %}
                  <div class="sb-card sb-p-6" 
                       data-storm="fade-in" 
                       data-storm-delay="{{ forloop.counter0|multiply:300
  }}">
                      <div class="sb-flex sb-items-center sb-mb-4">
                          <img src="{{ testimonial.avatar.url }}" 
                               class="sb-avatar sb-avatar-lg sb-mr-4"
                               data-storm="zoom-in" 
                               data-storm-delay="{{
  forloop.counter0|multiply:300|add:150 }}">
                          <div>
                              <p class="sb-font-semibold">{{
  testimonial.author }}</p>
                              <p class="sb-text-sm sb-text-secondary">{{
  testimonial.role }}</p>
                          </div>
                      </div>
                      <blockquote class="sb-quote" data-storm-hover="glow">
                          "{{ testimonial.quote }}"
                      </blockquote>
                  </div>
              {% endfor %}
          </div>
      </div>
  </section>

  Navigation Pattern with Spellbook

  {# navbar.html #}
  <nav class="sb-navbar sb-sticky sb-top-0 sb-z-50 sb-bg-surface 
  sb-shadow">
      <div class="sb-container sb-mx-auto sb-flex sb-justify-between 
  sb-items-center sb-px-4">
          <a href="/" class="sb-logo sb-text-2xl sb-font-bold 
  sb-text-primary" 
             data-storm="slide-right">
              {{ site.name }}
          </a>
          <ul class="sb-nav-menu sb-flex sb-space-x-6">
              {% for item in menu_items %}
                  <li data-storm="fade-in" 
                      data-storm-delay="{{
  forloop.counter0|multiply:100|add:200 }}"
                      data-storm-hover="lift">
                      <a href="{{ item.url }}" class="sb-nav-link 
  sb-text-secondary sb-hover:text-primary">
                          {{ item.title }}
                      </a>
                  </li>
              {% endfor %}
          </ul>
      </div>
  </nav>

  Forms Pattern with Spellbook

  {# contact_form.html #}
  <form method="post" class="sb-form sb-max-w-md sb-mx-auto" 
  data-storm="slide-up">
      {% csrf_token %}

      <div class="sb-form-group" data-storm="fade-in" 
  data-storm-delay="200">
          <label class="sb-label">{{ form.name.label }}</label>
          {{ form.name|add_class:"sb-input" }}
      </div>

      <div class="sb-form-group" data-storm="fade-in" 
  data-storm-delay="400">
          <label class="sb-label">{{ form.email.label }}</label>
          {{ form.email|add_class:"sb-input" }}
      </div>

      <div class="sb-form-group" data-storm="fade-in" 
  data-storm-delay="600">
          <label class="sb-label">{{ form.message.label }}</label>
          {{ form.message|add_class:"sb-textarea" }}
      </div>

      <button type="submit" 
              class="sb-btn sb-btn-primary sb-w-full"
              data-storm="fade-in" 
              data-storm-delay="800"
              data-storm-hover="lift"
              data-storm-click="pulse">
          Send Message
      </button>
  </form>

  🎯 Best Practices with Spellbook Classes

  1. Button Variations

  {# Primary button #}
  <button class="sb-btn sb-btn-primary" 
  data-storm-hover="lift">Primary</button>

  {# Secondary button #}
  <button class="sb-btn sb-btn-secondary" 
  data-storm-hover="scale">Secondary</button>

  {# Accent button #}
  <button class="sb-btn sb-btn-accent" 
  data-storm-hover="glow">Accent</button>

  {# Ghost button #}
  <button class="sb-btn sb-btn-ghost" 
  data-storm-hover="lift">Ghost</button>

  {# Button sizes #}
  <button class="sb-btn sb-btn-primary sb-btn-sm">Small</button>
  <button class="sb-btn sb-btn-primary sb-btn-lg">Large</button>

  2. Card Components

  {# Basic card #}
  <div class="sb-card sb-p-6" data-storm="fade-in">
      <h3 class="sb-card-title">Card Title</h3>
      <p class="sb-card-body">Card content</p>
  </div>

  {# Card with shadow #}
  <div class="sb-card sb-shadow-lg sb-p-6" data-storm="slide-up" 
  data-storm-hover="scale">
      {{ content }}
  </div>

  3. Grid Layouts

  {# Responsive grid #}
  <div class="sb-grid sb-grid-cols-1 sb-md:grid-cols-2 sb-lg:grid-cols-3 
  sb-gap-6">
      {% for item in items %}
          <div class="sb-card" data-storm="slide-up" 
               data-storm-delay="{{ forloop.counter0|multiply:150 }}">
              {{ item.content }}
          </div>
      {% endfor %}
  </div>

  4. Typography

  <h1 class="sb-text-6xl sb-font-bold sb-text-primary">Heading 1</h1>
  <h2 class="sb-text-4xl sb-font-semibold sb-text-secondary">Heading 2</h2>
  <p class="sb-text-lg sb-text-body">Body text</p>
  <span class="sb-text-sm sb-text-muted">Small text</span>

  🚫 What NOT to Do

  {# ❌ DON'T use generic classes #}
  <button class="btn btn-primary">  {# DON'T DO THIS #}

  {# ✅ DO use Spellbook classes #}
  <button class="sb-btn sb-btn-primary">  {# DO THIS #}

  {# ❌ DON'T mix Bootstrap/Tailwind classes #}
  <div class="card shadow-lg">  {# DON'T DO THIS #}

  {# ✅ DO use Spellbook equivalents #}
  <div class="sb-card sb-shadow-lg">  {# DO THIS #}

  📊 Common Patterns with Spellbook

  Pricing Cards

  {% for plan in pricing_plans %}
      <div class="sb-card sb-p-8 {% if plan.featured %}sb-border-primary{%
  endif %}"
           data-storm="slide-up" 
           data-storm-delay="{{ forloop.counter0|multiply:200 }}"
           data-storm-hover="scale">
          <h3 class="sb-text-2xl sb-font-bold">{{ plan.name }}</h3>
          <p class="sb-text-4xl sb-font-bold sb-text-primary sb-my-4">
              ${{ plan.price }}<span class="sb-text-lg 
  sb-text-muted">/mo</span>
          </p>
          <ul class="sb-list sb-mb-6">
              {% for feature in plan.features %}
                  <li class="sb-list-item">{{ feature }}</li>
              {% endfor %}
          </ul>
          <button class="sb-btn {% if plan.featured %}sb-btn-primary{% else
   %}sb-btn-secondary{% endif %} sb-w-full"
                  data-storm-hover="lift"
                  data-storm-click="pulse">
              Choose Plan
          </button>
      </div>
  {% endfor %}

  Alert Messages

  {# Success alert #}
  <div class="sb-alert sb-alert-success" data-storm="slide-down">
      <span class="sb-alert-icon">✓</span>
      {{ success_message }}
  </div>

  {# Error alert #}
  <div class="sb-alert sb-alert-error" data-storm="shake">
      <span class="sb-alert-icon">✕</span>
      {{ error_message }}
  </div>

  {# Warning alert #}
  <div class="sb-alert sb-alert-warning" data-storm="fade-in">
      <span class="sb-alert-icon">⚠</span>
      {{ warning_message }}
  </div>

  Footer with Spellbook

  <footer class="sb-footer sb-bg-dark sb-text-light sb-py-12">
      <div class="sb-container sb-mx-auto">
          <div class="sb-grid sb-grid-cols-1 sb-md:grid-cols-4 sb-gap-8">
              {% for column in footer_columns %}
                  <div data-storm="fade-in" data-storm-delay="{{
  forloop.counter0|multiply:200 }}">
                      <h4 class="sb-text-lg sb-font-semibold sb-mb-4">{{
  column.title }}</h4>
                      <ul class="sb-space-y-2">
                          {% for link in column.links %}
                              <li>
                                  <a href="{{ link.url }}" class="sb-link 
  sb-text-muted">
                                      {{ link.text }}
                                  </a>
                              </li>
                          {% endfor %}
                      </ul>
                  </div>
              {% endfor %}
          </div>
      </div>
  </footer>

  💡 Spellbook Classes Quick Reference

  | Component        | Spellbook Class                  | Description
          |
  |------------------|----------------------------------|------------------
  --------|
  | Button Primary   | sb-btn sb-btn-primary            | Main CTA button
          |
  | Button Secondary | sb-btn sb-btn-secondary          | Secondary action
          |
  | Button Accent    | sb-btn sb-btn-accent             | Special emphasis
          |
  | Card             | sb-card                          | Content container
          |
  | Grid             | sb-grid sb-grid-cols-{n}         | Responsive grid
          |
  | Container        | sb-container                     | Max-width wrapper
          |
  | Text Sizes       | sb-text-{size}                   | xs, sm, lg, xl,
  2xl, etc |
  | Spacing          | sb-p-{n}, sb-m-{n}               | Padding/margin
          |
  | Shadow           | sb-shadow-{size}                 | sm, md, lg, xl
          |
  | Colors           | sb-text-primary, sb-bg-surface   | Theme colors
          |
  | Forms            | sb-input, sb-textarea, sb-select | Form elements
          |
  | Alerts           | sb-alert sb-alert-{type}         | Notifications
          |

  🔧 Complete Example Page

  {# landing_page.html #}
  {% extends "base.html" %}
  {% load static %}

  {% block content %}
  <!-- Hero Section -->
  <section class="sb-hero sb-bg-gradient sb-py-20">
      <div class="sb-container sb-mx-auto sb-text-center">
          <h1 class="sb-text-6xl sb-font-bold sb-text-white" 
              data-storm="hero-title">
              {{ hero.title }}
          </h1>
          <p class="sb-text-xl sb-text-white-80 sb-mt-4 sb-max-w-2xl 
  sb-mx-auto"
             data-storm="hero-subtitle" 
             data-storm-delay="300">
              {{ hero.subtitle }}
          </p>
          <div class="sb-flex sb-justify-center sb-gap-4 sb-mt-8">
              <button class="sb-btn sb-btn-primary sb-btn-lg"
                      data-storm="fade-in" 
                      data-storm-delay="600"
                      data-storm-hover="lift"
                      data-storm-click="pulse">
                  Get Started Free
              </button>
              <button class="sb-btn sb-btn-ghost sb-btn-lg sb-text-white"
                      data-storm="fade-in" 
                      data-storm-delay="800"
                      data-storm-hover="scale">
                  Learn More
              </button>
          </div>
      </div>
  </section>

  <!-- Features Section -->
  <section class="sb-section sb-py-16">
      <div class="sb-container sb-mx-auto">
          <h2 class="sb-text-4xl sb-font-bold sb-text-center sb-mb-12"
              data-storm="fade-in">
              Why Choose Us
          </h2>
          <div class="sb-grid sb-grid-cols-1 sb-md:grid-cols-3 sb-gap-8">
              {% for feature in features %}
                  <div class="sb-card sb-p-6 sb-text-center"
                       data-storm="slide-up"
                       data-storm-delay="{{ forloop.counter0|multiply:200
  }}"
                       data-storm-hover="scale">
                      <div class="sb-icon-wrapper sb-bg-primary-light 
  sb-rounded-full sb-w-16 sb-h-16 sb-mx-auto sb-mb-4"
                           data-storm-click="bounce">
                          <i class="sb-icon sb-icon-{{ feature.icon }} 
  sb-text-3xl sb-text-primary"></i>
                      </div>
                      <h3 class="sb-text-xl sb-font-semibold sb-mb-2">{{
  feature.title }}</h3>
                      <p class="sb-text-secondary">{{ feature.description
  }}</p>
                  </div>
              {% endfor %}
          </div>
      </div>
  </section>

  <!-- CTA Section -->
  <section class="sb-section sb-bg-primary sb-py-16">
      <div class="sb-container sb-mx-auto sb-text-center">
          <h2 class="sb-text-3xl sb-font-bold sb-text-white"
              data-storm="fade-in">
              Ready to Get Started?
          </h2>
          <p class="sb-text-lg sb-text-white-80 sb-mt-4"
             data-storm="fade-in" 
             data-storm-delay="200">
              Join thousands of satisfied customers
          </p>
          <button class="sb-btn sb-btn-white sb-btn-lg sb-mt-8"
                  data-storm="fade-in"
                  data-storm-delay="400"
                  data-storm-hover="lift"
                  data-storm-click="sparkles">
              Start Your Free Trial
          </button>
      </div>
  </section>
  {% endblock %}

  📝 Remember

  Your role is to create beautiful, animated Django websites using:
  1. Storm System HTML attributes for animations (data-storm,
  data-storm-hover, data-storm-click)
  2. Django Spellbook sb- classes for styling and layout
  3. NO custom CSS or JavaScript - everything is handled by the frameworks

  The combination of Storm System animations and Spellbook's design system
  creates professional, consistent, and beautiful websites with minimal
  effort!
