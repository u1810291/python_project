from bs4 import BeautifulSoup
from flask import request


def is_json_ajax():
    return request.is_json and request.is_xhr


def html_to_text(html):
    if html is None or not isinstance(html, (str, unicode)):
        return None

    return BeautifulSoup(html, "html.parser").text
