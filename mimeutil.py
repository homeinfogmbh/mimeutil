"""MIME type and file extensions handling."""

from __future__ import annotations
from hashlib import sha256
from io import BufferedIOBase, IOBase, RawIOBase, TextIOBase
from mimetypes import guess_extension
from pathlib import Path
from typing import Any, Iterable, NamedTuple, Union

from magic import detect_from_content, detect_from_filename, detect_from_fobj
from magic.compat import FileMagic


__all__ = [
    'FILE_EXTENSIONS',
    'MIME_TYPES',
    'mimetype',
    'mimetype_to_ext',
    'ext_to_mimetype',
    'getext',
    'is_xml',
    'FileMetaData'
]


FILE_LIKE_OBJECTS = (BufferedIOBase, IOBase, RawIOBase, TextIOBase)
FILE_EXTENSIONS = {  # Most common MIME types for fast lookup.
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'video/x-msvideo': '.avi',
    'video/mpeg': '.mpg',
    'video/quicktime': '.mov',
    'video/x-flv': '.flv',
    'application/pdf': '.pdf',
    'application/xml': '.xml',
    'text/html': '.html',
    'text/xml': '.xml'
}
MIME_TYPES = {suffix: mimetype for mimetype, suffix in FILE_EXTENSIONS.items()}
XML_MIMETYPES = {'application/xml', 'text/xml'}
File = Union[bytes, str, Path, BufferedIOBase, IOBase, RawIOBase, TextIOBase]


def _file_magic(file: File) -> FileMagic:
    """Returns the file magic namedtuple from the respective file."""

    if isinstance(file, bytes):
        return detect_from_content(file[:1024])     # Fix issue #350.

    if isinstance(file, str):
        return _file_magic(Path(file))

    if isinstance(file, Path):
        if file.is_file():
            return detect_from_filename(str(file))

        raise FileNotFoundError(str(file))

    if isinstance(file, FILE_LIKE_OBJECTS):
        return detect_from_fobj(file)

    raise TypeError(f'Cannot read MIME type from {type(file)}.')


def mimetype(file: File) -> str:
    """Guess MIME type of file."""

    return _file_magic(file).mime_type


def mimetype_to_ext(mime_type: str) -> str:
    """Returns the extension for a given MIME type."""

    try:
        return FILE_EXTENSIONS[mime_type]
    except KeyError:
        return guess_extension(mime_type) or ''


def ext_to_mimetype(suffix: str) -> str:
    """Returns the MIME type to a file extension."""

    return MIME_TYPES.get(suffix.lower(), '')


def getext(file: File) -> str:
    """Guess a file suffix for the given file."""

    return mimetype_to_ext(mimetype(file))


def is_xml(file: File) -> bool:
    """Determines whether the file is an XML file."""

    return mimetype(file) in XML_MIMETYPES


class FileMetaData(NamedTuple):
    """Represents file meta data."""

    sha256sum: str
    mimetype: str
    suffix: str

    @classmethod
    def from_bytes(cls, data: bytes) -> FileMetaData:
        """Creates file meta data from the respective bytes."""
        return cls(sha256(data).hexdigest(), (mime_type := mimetype(data)),
                   mimetype_to_ext(mime_type))

    @property
    def filename(self) -> str:
        """Returns a unique file name from the SHA-256 hash and suffix."""
        return self.sha256sum + self.suffix

    def keys(self) -> Iterable[str]:
        """Yields the keys."""
        return self._fields     # pylint: disable=E1101

    def __getitem__(self, item: Union[int, str]) -> Any:
        """Returns the respective item."""
        if isinstance(item, int):
            return NamedTuple.__getitem__(self, item)   # pylint: disable=E1101

        if isinstance(item, str):
            return getattr(self, item)

        raise TypeError('Item must be int or str.')
