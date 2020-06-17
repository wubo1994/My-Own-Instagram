import re

from django import template
from django.urls import NoReverseMatch, reverse
from Instagram.models import Like, UserConnection


register = template.Library()


@register.simple_tag
def user_liked_post(user, post):
    try:
        like = Like.objects.get(post=post, user=user)
        return "fa-heart"
    except:
        return "fa-heart-o"

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''

@register.simple_tag
def is_following(user1, user2):
    return user2.get_followers().filter(follower=user1).exists()