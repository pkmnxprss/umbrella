from django import template

# template.Library registers all template tags and filters.
# So here we can add our new filter to them
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
