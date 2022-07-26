from django import template  # template.Library registers all template tags and filters

register = template.Library()  # add our new filter to them


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})
