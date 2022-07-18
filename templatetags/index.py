from django import template
import json


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
    print(json.loads(value))
    return json.loads(value)
