from django import template

register = template.Library()

@register.filter(name='static_responsive')
def get_responsive_url_static(url):
    return "%s___asnf874wthwengsfduy" % url
