"""Provides the `Subtitle` class."""

from .subtitle import Subtitle
from . import writers

from pathlib import Path


class Subtitles:
    """
    Represents a sequence of subtitles.

    Example:
    ```
    >>> import subsy
    >>> subtitles = subsy.load('reference.srt')
    >>> len(subtitles)
    """

    def __init__(self, subtitles=None, source=None):
        if subtitles is None:
            subtitles = []
        elif not isinstance(subtitles, list):
            raise TypeError('Argument "subtitles" must be a list.')
        if any(not isinstance(item, Subtitle) for item in subtitles):
            raise TypeError('Argument "subtitles" must only contain '
                            'Subtitle objects.')
        if source is None:
            source = {}
        self.subtitles = subtitles
        """List of `Subtitle` instances that make up the sequence."""
        previous = None
        index = 0
        for subtitle in self.subtitles:
            index += 1
            subtitle.parent = self
            subtitle.index  = index
            if previous:
                previous.next = subtitle
            subtitle.previous = previous
            previous = subtitle
        self.source = source
        """
        Dictionary holding meta information about the subtitles's source.

        This is usually a file, and the dictionary would contain a key
        named `'file'` with a `pathlib.Path` object for its value pointing
        to the file-system location that the subtitles were loaded from.
        A second key named `'encoding'` would store the text encoding,
        as automatically detected by `subsy.load()` or passed in to it
        specifically.

        These two entries, if they exist, are used by the `save()` method
        to update the file (if called without arguments).
        """

    def __iter__(self):
        yield from self.subtitles

    def __len__(self):
        return len(self.subtitles)

    def __contains__(self, value):
        if isinstance(value, Subtitle):
            return (value in self.subtitles)
        elif isinstance(value, str):
            return any(value in subtitle for subtitle in self)
        else:
            return False

    def __getitem__(self, key):
        return self.subtitles[key]

    def __setitem__(self, key, value):
        if isinstance(value, Subtitle):
            self.subtitles[key] = value
        elif isinstance(value, str):
            self.subtitles[key].text = value
        elif isinstance(value, list):
            self.subtitles[key].lines = value
        else:
            name = type(value).__name__
            raise TypeError(f'Cannot assign a value of type "{name}."')

    def __eq__(self, other):
        if isinstance(other, Subtitles):
            return self.subtitles == other.subtitles
        else:
            return NotImplemented

    def __str__(self):
        if 'file' in self.source:
            return self.source['file'].stem
        else:
            return '<unnamed>'

    def __repr__(self):
        klass = self.__class__.__name__
        if 'file' in self.source:
            file = self.source['file'].name
        else:
            file = '<unnamed>'
        return f'{klass}({file})'

    def save(self, file=None, encoding=None, format=None):
        """
        Saves the subtitles to disk.

        An optional `file` can be specified (as a `pathlib.Path` object
        or string) to indicate the path and file name. If not given,
        the `'file'` reference will be retrieved from the meta information
        stored in the `source` attribute. Failing that, a `ValueError`
        is raised.

        An optional `encoding` can be specified. All [valid encoding
        names][encodings] are supported. If not given, the value for
        `'encoding'` will be retrieved from the `source` meta info.
        If the key is not found, it defaults to `'UTF-8-sig'`, i.e.
        variable-length Unicode with signature / byte-order mark.

        An optional `format` can be specified, which would otherwise
        be deduced from the file ending.

        [encodings]: https://docs.python.org/3/library/codecs.html
        """
        if not file:
            file = self.source.get('file', None)
            if not file:
                raise ValueError('Specify a file name to save to.')
        file = Path(file)
        if not encoding:
            encoding = self.source.get('encoding', 'UTF-8-sig')
        writers.save(self, file, encoding, format)
