import logging

from .base import ResponseFilter


class ContentTypeFilter(ResponseFilter):

    def __init__(self, content_type):
        self.content_type = content_type

    def run(self, res):
        if self.content_type in res.response.headers["content-type"]:
            yield res
        else:
            logging.warning(f"Filtered out: {res.request.url}. "
                            f"Content type didn't match {self.content_type}")
