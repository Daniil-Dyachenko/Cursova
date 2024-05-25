from django import template
from django.utils.http import urlencode

from sushi.models import Categories

register = template.Library()


@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    get = context['request'].GET.dict()
    get.update(kwargs)
    return urlencode(get)