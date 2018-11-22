"""MIME type and file extensions handling."""

from collections import namedtuple
from hashlib import sha256

from mimetypes import guess_extension
from magic import from_file, from_buffer

__all__ = ['MIME_TYPES', 'mimetype', 'getext', 'FileMetaData']


MIME_TYPES = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'video/x-msvideo': '.avi',
    'video/mpeg': '.mpg',
    'video/quicktime': '.mov',
    'video/x-flv': '.flv',
    'application/pdf': '.pdf',
    'application/xml': '.xml',
    'text/html': '.html'}


def mimetype(file):
    """Guess MIME type of file."""

    try:
        return from_file(file, mime=True)
    except (OSError, TypeError, ValueError):
        try:
            data = file.read()
        except AttributeError:
            return from_buffer(file, mime=True)
        else:
            return from_buffer(data, mime=True)


def getext(file):
    """Guess a file suffix for the MIME type or file."""

    mime_type = mimetype(file)

    try:
        return MIME_TYPES[mime_type]
    except KeyError:
        return guess_extension(mime_type) or ''


class FileMetaData(namedtuple('FileMetaData', 'sha256sum mimetype suffix')):
    """Represents file meta data."""

    __slots__ = ()

    @classmethod
    def from_bytes(cls, data):
        """Creates file meta data from the respective bytes."""
        return cls(sha256(data).hexdigest(), mimetype(data), getext(data))

    @property
    def filename(self):
        """Returns a unique file name from the SHA-256 hash and suffix."""
        return self.sha256sum + self.suffix
