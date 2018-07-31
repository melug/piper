import re
#  import logging
import requests

from piper.base import Resource, Download
from piper.html import ParseHtml, ExtractResources, ExtractText


#  logging.basicConfig(level=logging.INFO)


def simple_resource(url):
    return Resource(requests.Request("GET", url), None, requests.Session(), {})


if __name__ == "__main__":
    home_page = simple_resource("http://ikon.mn")
    download_and_parse_html = Download() | ParseHtml()
    p = download_and_parse_html | \
        ExtractResources(css_selector="ul.newslist div.nltitle a") | \
        download_and_parse_html | \
        ExtractText(css_selector="div.icontent")
    for res in p.flow([home_page]):
        print(f'URL: {res.request.url}')
        print('\n'.join([re.sub(r'\s{2,}', '\n', e.text_content().strip())
                         for e in res.meta['text']]))
