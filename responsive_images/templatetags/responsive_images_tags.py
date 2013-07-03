from django.template import Library, Node, NodeList, Variable
from django.conf import settings

register = Library()


@register.simple_tag()
def static_responsive(url):
    url = "%s%s" % (url, settings.IMAGE_ENDS_WITH)
    return url
