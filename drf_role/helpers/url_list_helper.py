from django.conf import settings
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

__author__ = 'Ashraful'

URL_NAMES = []


def get_all_url_names(urlpatterns):
    """
    :param urlpatterns: django url formatted patterns
    :return: global var URL_NAMES
    """
    for pattern in urlpatterns:
        # Check it resolver or pattern. If pattern then end level if not ? then, go deeper level
        if isinstance(pattern, RegexURLResolver):
            # Check if the url custom url or django default. Actually making diff by namespace.
            # So, You are not allowed to put namespace on your urls
            if pattern.namespace is not None:
                continue
            # Recursive call for going deeper to find out regex patterns
            get_all_url_names(pattern.url_patterns)  # call this function recursively
        elif isinstance(pattern, RegexURLPattern):
            url_name = pattern.name  # get the view name
            if url_name:
                URL_NAMES.append(url_name)
    return URL_NAMES


def get_urls(*args, **kwargs):
    """
    :param args: expecting any tuple (still not implemented)
    :param kwargs: expecting any dictionary like object (still not implemented)
    :return: a function call as a list
    """
    global URL_NAMES
    URL_NAMES = []
    root_urlconf = __import__(settings.ROOT_URLCONF)  # import root_urlconf module
    all_urlpatterns = root_urlconf.urls.urlpatterns
    get_all_url_names(all_urlpatterns)
    return URL_NAMES
