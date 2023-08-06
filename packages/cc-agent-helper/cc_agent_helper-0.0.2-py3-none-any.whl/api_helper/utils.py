import random
from urllib.parse import urlparse
from . import settings


def get_uri(uri='', base=None):
    return '{}{}'.format(base, uri)


def get_base_url(origin):
    url = urlparse(origin)  # type: ParseResult
    return url.scheme + "://" + url.netloc + '/'


def patch_header(session, header=None):
    if header is None:
        header = settings.DEFAULT_HEADERS
    session.headers.update(header)


def random_ip(session, base_ip='116.118.{}.{}'):
    session.headers.update({
        'X-Forwarded-For': base_ip.format(random.randrange(200), random.randrange(200))
    })
