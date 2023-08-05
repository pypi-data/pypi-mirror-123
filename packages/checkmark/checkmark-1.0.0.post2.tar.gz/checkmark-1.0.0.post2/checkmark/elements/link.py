import re

from collections import namedtuple



Link = namedtuple('Link', ['text', 'url', 'title'])


def url_safe(text: str) -> str:
    """Replace characters that are not URL-safe into dashes"""
    return re.sub(r'[^(a-z)(A-Z)(0-9)._-]+', '-', text)


def link(string: str) -> Link:
    """Generate text, url and title from string"""

    # If formatted as a link, return the features
    if m := re.match(r'\[(.*)\]\((.+?)(?: \"(.*)\")?\)', string):
        text = m.group(1)
        url = url_safe(m.group(2))
        title = m.group(3) or None

    # Otherwise, generate features from the text
    else:
        text = string
        url = url_safe(string)
        title = None

    return Link(text, url, title)