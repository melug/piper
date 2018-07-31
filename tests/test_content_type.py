import unittest

import requests

from piper.base import Resource, Download
from piper.http import ContentTypeFilter
from piper.html import ParseHtml, ExtractResources


def simple_resource(url):
    return Resource(requests.Request("GET", url), None, requests.Session(), {})


class ContentTypeTest(unittest.TestCase):

    def test_content_types(self):
        pages = [simple_resource("http://example.com"),
                 simple_resource("http://ikon.mn"),
                 simple_resource("https://code.jquery.com/jquery-3.3.1.js")]
        filter_html = ContentTypeFilter("text/html")
        download_filter_html = Download() | filter_html
        self.assertEqual(len(list(download_filter_html.flow(pages))), 2)

        filter_js = ContentTypeFilter("application/javascript")
        download_filter_js = Download() | filter_js
        self.assertEqual(len(list(download_filter_js.flow(pages))), 1)


class HtmlLinkExtractTest(unittest.TestCase):

    def test_extract_links(self):
        home_page = simple_resource("http://ikon.mn")
        p = Download() | ParseHtml() | \
            ExtractResources(css_selector="ul.newslist div.nltitle a")
        self.assertEqual(len(list(p.flow([home_page]))), 50)
