from django import template
import json
from webPages.config import KAKAO_JAVA_KEY


register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_type(value):
    return type(value)


@register.filter
def to_json(value):
    return json.loads(value)


@register.filter
def java_key(value):
    return KAKAO_JAVA_KEY


@register.filter
def page(paginator, value):
    return paginator.get_page(value)
