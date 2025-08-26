from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ forloop.counter0|multiply:100 }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0