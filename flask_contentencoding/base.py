from flask import request


class BaseEncoder(object):
    content_encoding = None
    content_type_blacklist = [
        'image/*',
        'video/*',
        'application/pdf',
    ]

    def __init__(self, minimum_size=400, content_type_blacklist=None):
        self.minimum_size = minimum_size
        if content_type_blacklist is not None:
            self.content_type_blacklist = content_type_blacklist

    def after_request(self, response):
        if self.should_compress(response):
            response.data = self.compress(response.data)
            response.headers['Content-Encoding'] = self.content_encoding
            response.headers['Content-Length'] = len(response.data)
        return response

    def should_compress(self, response):
        content_type = response.headers.get('Content-Type', None)

        return all([
            self.content_encoding.lower() in request.headers.get('Accept-Encoding', '').lower(),
            len(response.data) >= self.minimum_size,
            not any([
                content_type in self.content_type_blacklist,
                content_type.split('/')[0] + '/*' in self.content_type_blacklist,
            ]),
        ])