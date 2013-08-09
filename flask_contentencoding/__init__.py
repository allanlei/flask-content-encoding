from flask import request

from .gzip import Gzip
from .deflate import Deflate

class ContentEncoder(object):
    def __init__(self, app, *args, **kwargs):
        if app:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, content_type_blacklist=None, encoders=[Gzip(), Deflate()]):
        self.app = app
        if content_type_blacklist is not None:
            self.content_type_blacklist = content_type_blacklist
        self.encoders = dict([(encoder.content_encoding, encoder) for encoder in encoders])
        self.app.after_request(self.after_request)

    def after_request(self, response):
        for accepted_content_encoding in request.headers.get('Accept-Encoding', '').lower().split(','):
            if not self.should_encode(response):
                break

            if accepted_content_encoding in self.encoders.keys():
                encoder = self.encoders[accepted_content_encoding]
                response = encoder.after_request(response)
        return response

    def should_encode(self, response):
        return all([
            'Content-Encoding' not in response.headers,
            (200 <= response.status_code < 300),
        ])