

class Processor:

    def run(self, obj):
        pass

    def __or__(self, other):
        return Pipe([self, other])


class Pipe(Processor):

    def __init__(self, processors):
        self.processors = processors

    def run(self, obj):
        result = obj
        for p in self.processors:
            result = p.run(result)
        return result


class Download(Processor):

    def run(self, obj):
        obj['response'] = 'Example response'
        return obj


class Store(Processor):

    def run(self, obj):
        obj['saved_date'] = '2018/09/03'
        return obj


class Map(Processor):

    def __init__(self, processor):
        self.processor = processor

    def run(self, objects):
        for obj in objects:
            yield self.processor.run(obj)


class Filter(Processor):

    def run(self, obj):
        pass


class PDF(Processor):

    def run(self, obj):
        pass


download_and_store = Download() | Store()
#  filter_pdf_processor = download_and_store | Filter(content_type='pdf') | PDF()
print(download_and_store.run({"url": "http://example.com"}))
