from .base import BaseEncoder

import zlib

class Deflate(BaseEncoder):
    content_encoding = 'deflate'

    def compress(self, data):
        return zlib.compress(data)