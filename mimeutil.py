"""MIME type and file extensions handling."""

from hashlib import sha256
from io import BufferedIOBase, IOBase, RawIOBase, TextIOBase
from mimetypes import guess_extension
from pathlib import Path
from typing import NamedTuple

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


def _file_magic(file):
    """Returns the file magic namedtuple from the respective file."""

    if isinstance(file, bytes):
        return detect_from_content(file)

    if isinstance(file, str):
        return _file_magic(Path(file))

    if isinstance(file, Path):
        if file.is_file():
            return detect_from_filename(str(file))

        raise FileNotFoundError(str(file))

    if isinstance(file, FILE_OBJECTS):
        return detect_from_fobj(file)

    raise ValueError('Cannot read MIME type from %s.' % type(file))


def mimetype(file):
    """Guess MIME type of file."""

    return _file_magic(file).mime_type


def getext(file):
    """Guess a file suffix for the MIME type or file."""

    mime_type = mimetype(file)

    try:
        return MIME_TYPES[mime_type]
    except KeyError:
        return guess_extension(mime_type) or ''


class FileMetaData(NamedTuple):
    """Represents file meta data."""

    sha256sum: str
    mimetype: str
    suffix: str

    @classmethod
    def from_bytes(cls, data):
        """Creates file meta data from the respective bytes."""
        return cls(sha256(data).hexdigest(), mimetype(data), getext(data))

    @property
    def filename(self):
        """Returns a unique file name from the SHA-256 hash and suffix."""
        return self.sha256sum + self.suffix
