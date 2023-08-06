import random
from urllib.parse import urlparse
from . import settings


def get_uri(uri, base):
    return '{}{}'.format(base, uri)


def get_base_url(origin):
    url = urlparse(origin)  # type: ParseResult
    return url.scheme + "://" + url.netloc + '/'


def patch_header(session):
    session.headers.update(settings.DEFAULT_HEADERS)


def random_ip(session):
    _ip = '116.118.{}.{}'.format(random.randrange(200), random.randrange(200))
    session.headers.update({
        'X-Forwarded-For': _ip
    })
