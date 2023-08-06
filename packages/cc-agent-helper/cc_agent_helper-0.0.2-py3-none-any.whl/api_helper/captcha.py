import io

import requests

from . import settings


def captcha_solver(img, **kwargs):
    if isinstance(img, str):
        img = io.StringIO(img)

    if isinstance(img, bytes):
        img = io.BytesIO(img)

    r = requests.post(settings.CAPTCHA_API, data=kwargs, files=dict(file=img))

    return r.text


__all__ = ('captcha_solver',)
