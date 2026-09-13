from django import template
from products.models import Class

register = template.Library()

@register.inclusion_tag('includes/category_list.html')
def render_classes():
    classes = Class.objects.all()
    return {'classes': classes}
