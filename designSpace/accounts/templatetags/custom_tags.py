from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Generates a range of numbers for iteration in templates."""
    try:
        value = int(value)
        return range(value)
    except (ValueError, TypeError):
        return []