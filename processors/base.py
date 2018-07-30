import logging

from recordclass import recordclass


Resource = recordclass('Resource', ['request', 'response', 'session'])


class Processor:

    def run(self, res):
        """ Takes single resource and returns multiple resources """
        raise NotImplementedError

    def flow(self, ress):
        """ Run transformation on for each resource """
        for res in ress:
            yield from self.run(res)

    def __or__(self, other):
        return Pipe([self, other])


class Pipe(Processor):

    def __init__(self, processors):
        self.processors = processors

    def run(self, res):
        """ Pipes list of resources from one processor into another """
        results = [res]
        for p in self.processors:
            results = p.flow(results)
        return results


class Download(Processor):

    def run(self, res):
        rq, ss = res.request, res.session
        logging.info(f"Checking url: {rq.url}")
        res.response = ss.send(ss.prepare_request(rq), allow_redirects=True)
        yield res


class Filter(Processor):

    def __init__(self, f):
        self.f = f


class ResponseFilter(Filter):

    def run(self, res):
        if self.f(res.response):
            yield res.response


class RequestFilter(Filter):
    """ Who uses this? """

    def run(self, res):
        if self.f(res.request):
            yield res.request
