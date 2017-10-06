"""MIME type and file extensions handling."""

from mimetypes import guess_extension
from magic import from_file, from_buffer

__all__ = ['MIME_TYPES', 'mimetype', 'getext']


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


def getext(mimetype_or_file):
    """Guess a file suffix for the MIME type or file."""

    try:
        return MIME_TYPES[mimetype_or_file]
    except KeyError:
        mime_type = mimetype(mimetype_or_file)

        try:
            return MIME_TYPES[mime_type]
        except KeyError:
            return guess_extension(mime_type) or ''
