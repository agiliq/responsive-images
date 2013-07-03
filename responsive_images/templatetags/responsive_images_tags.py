from django.template import Library, Node, NodeList, Variable

register = Library()


@register.simple_tag()
def static_responsive(url):
    url = "%s___asnf874wthwengsfduy" % url
    return url
