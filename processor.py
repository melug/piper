import requests
from collections import namedtuple


Resource = namedtuple('Resource', ['request', 'response'])


class Processor:

    def run(self, res):
        raise NotImplementedError

    def __or__(self, other):
        return Pipe([self, other])


class Pipe(Processor):

    def __init__(self, processors):
        self.processors = processors

    def run(self, res):
        result = res
        for p in self.processors:
            result = p.run(result)
        return result


class Download(Processor):

    def run(self, res):
        return Resource(res.request, requests.get(res.request))


class Store(Processor):

    def __init__(self, storage):
        self.storage = storage

    def run(self, res):
        with open(self.storage, 'w') as f:
            f.write(res.response.text)
        return res


class Map(Processor):

    def __init__(self, processor):
        self.processor = processor

    def run(self, resources):
        for res in resources:
            yield self.processor.run(res)


class Filter(Processor):

    def run(self, res):
        pass


class PDF(Processor):

    def run(self, res):
        pass


if __name__ == "__main__":
    download_and_store = Download() | Store("data.txt")
    print(download_and_store.run(Resource("http://example.com", None)))
