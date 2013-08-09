from .base import BaseEncoder

import gzip

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


class Gzip(BaseEncoder):
    content_encoding = 'gzip'

    def __init__(self, *args, **kwargs):
        self.compress_level = kwargs.pop('compress_level', 6)
        self.buffer_class = kwargs.pop('buffer_class', StringIO)
        super(Gzip, self).__init__(*args, **kwargs)

    def compress(self, data):
        gzip_buffer = self.buffer_class()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=self.compress_level, fileobj=gzip_buffer)
        gzip_file.write(data)
        gzip_file.close()
        return gzip_buffer.getvalue()