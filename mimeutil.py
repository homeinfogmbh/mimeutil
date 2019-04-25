"""MIME type and file extensions handling."""

from collections import namedtuple
from hashlib import sha256
from io import BufferedIOBase, IOBase, RawIOBase, TextIOBase
from mimetypes import guess_extension
from pathlib import Path

from magic import detect_from_content, detect_from_filename, detect_from_fobj


__all__ = ['MIME_TYPES', 'mimetype', 'getext', 'FileMetaData']


FILE_OBJECTS = (BufferedIOBase, IOBase, RawIOBase, TextIOBase)
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

    if isinstance(file, bytes):
        file_magic = detect_from_content(file)
    elif isinstance(file, str):
        file_magic = detect_from_filename(file)
    elif isinstance(file, Path):
        file_magic = detect_from_filename(str(file))
    elif isinstance(file, FILE_OBJECTS):
        file_magic = detect_from_fobj(str(file))
    else:
        raise ValueError('Cannot read MIME type from %s.' % type(file))

    return file_magic.mime_type


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
