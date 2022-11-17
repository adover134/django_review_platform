from django import template
import json
import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from webPages.config import SOCIAL_AUTH_KAKAO_KEY, KAKAO_JAVA_KEY


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
def loginkey(value):
    return SOCIAL_AUTH_KAKAO_KEY


@register.filter
def page(paginator, value):
    return paginator.get_page(value)


@register.filter
def check_active(user):
    if user.uActive == 1:
        state = str(user.penaltyDate+relativedelta(days=7))+'까지 신고 불가'
    elif user.uActive == 2:
        state = str(user.penaltyDate+relativedelta(days=30))+'까지 신고 불가'
    if user.uActive == 3:
        state = str(user.penaltyDate+relativedelta(days=30))+'까지 리뷰 수정/삭제 및 신고 불가'
    else:
        state = '모든 기능 사용 가능'
    return state


@register.filter
def sets(lists):
    return sorted(list(set(lists)))


@register.filter
def defaultImage(image, s):
    img = json.loads(requests.get(image).text)
    if image is not None and os.path.isfile(os.path.join('static/images/'+s+'Image/', img.get('image'))):
        return img.get('image')
    else:
        return 'no-photo.png'


@register.filter
def check_url(url):
    if url.find('change') > -1 or url.find('write') > -1:
        return None
    else:
        return url


@register.filter
def ranges(integer):
    return range(integer)
