from requests import Request
from requests.compat import urljoin
from lxml.html import fromstring

from .base import Processor, Resource
from .http import ContentTypeFilter


html_filter = ContentTypeFilter("text/html")


class ParseHtml(Processor):

    def run(self, res):
        res.meta['html'] = fromstring(res.response.content)
        yield res


class ExtractElement(Processor):

    def __init__(self, css_selector='a'):
        self.css_selector = css_selector


class ExtractResources(ExtractElement):
    """ Actually link extractor """

    def run(self, res):
        for a in res.meta['html'].cssselect(self.css_selector):
            new_link = urljoin(res.request.url, a.attrib['href'])
            yield Resource(Request('GET', new_link), None, res.session, {})


class ExtractText(ExtractElement):

    def run(self, res):
        res.meta['text'] = res.meta['html'].cssselect(self.css_selector)
        yield res


class DumpText(Processor):

    def run(self, res):
        print(f"URL: {res.request.url}, text:")
        print(res.meta['text'])
        yield res
