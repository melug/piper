import requests
from requests.utils import urlparse
from recordclass import recordclass


Resource = recordclass('Resource', ['request', 'response', 'session'])


class Processor:

    def run(self, res):
        """ Takes single resource and returns multiple resources """
        raise NotImplementedError

    def flow(self, ress):
        """ Pipes list of resources from one processor into another """
        for res in ress:
            yield from self.run(res)

    def __or__(self, other):
        return Pipe([self, other])


class Pipe(Processor):

    def __init__(self, processors):
        self.processors = processors

    def run(self, res):
        results = [res]
        for p in self.processors:
            results = p.flow(results)
        return results


class Download(Processor):

    def run(self, res):
        rq, ss = res.request, res.session
        res.response = ss.send(ss.prepare_request(rq))
        yield res


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


class Map(Processor):

    def __init__(self, processor):
        self.processor = processor

    def run(self, resources):
        for res in resources:
            yield self.processor.run(res)


class Filter(Processor):

    def __init__(self, f):
        self.f = f

    def run(self, res):
        pass


class PDF(Processor):

    def run(self, res):
        pass


if __name__ == "__main__":
    example = Resource(requests.Request("GET", "http://example.com"),
                       None,
                       requests.Session())
    ikon = Resource(requests.Request("GET", "http://ikon.mn"),
                    None,
                    requests.Session())
    initials = [example, ikon]
    download_and_store = Download() | UrlStampedStorage()
    results = download_and_store.flow(initials)
    print(list(results))
