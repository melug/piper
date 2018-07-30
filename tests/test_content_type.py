import unittest

import requests

from processors.base import Resource, Download
from processors.http import ContentTypeFilter


def simple_resource(url):
    return Resource(requests.Request("GET", url), None, requests.Session())


class ContentTypeTest(unittest.TestCase):

    def test_content_types(self):
        pages = [simple_resource("http://example.com"),
                 simple_resource("http://ikon.mn"),
                 simple_resource("https://code.jquery.com/jquery-3.3.1.js")]
        html_filter = ContentTypeFilter("text/html")
        self.assertEqual(len(list((Download() | html_filter).flow(pages))), 2)

        js_filter = ContentTypeFilter("application/javascript")
        self.assertEqual(len(list((Download() | js_filter).flow(pages))), 1)
