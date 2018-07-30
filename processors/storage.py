import requests
from requests.utils import urlparse

from processors.base import Processor


class Store(Processor):

    def __init__(self, storage):
        self.storage = storage

    def run(self, res):
        with open(self.storage, 'w') as f:
            f.write(res.response.text)
        yield res


class UrlStampedStorage(Processor):

    def run(self, res):
        scheme, netloc, path, params, query, fragment = urlparse(res.request.url)
        with open(netloc, 'w') as f:
            f.write(res.response.text)
        yield res
