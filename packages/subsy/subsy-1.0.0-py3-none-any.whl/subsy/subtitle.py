"""Provides the `Subtitle` class."""

from . import timestamp

import re


class Subtitle:
    r"""
    Represents a single subtitle.

    Example:
    ```
    >>> import subsy
    >>> subtitle = subsy.Subtitle(['First line.', 'Line <i>with</i> markup.'])
    >>> subtitle.lines
    ['First line.', 'Line <i>with</i> markup.']
    >>> subtitle.text
    'First line.\nLine <i>with</i> markup.'
    >>> subtitle.plain
    'First line.\nLine with markup.'
    >>> subtitle.start
    0
    >>> subtitle.start_time
    '00:00:00.000'
    >>> subtitle.end_time
    '00:00:01.000'
    >>> subtitle.end_time = '00:00:02.000'
    >>> subtitle.end
    2000
    ```
    """

    def __init__(self, lines=None, start=0, duration=1000,
                 parent=None, index=None, next=None, previous=None):
        if lines is None:
            lines = []
        self.lines = lines
        """List of individual lines of the subtitle's text."""
        self.start = start
        """Start time in milliseconds."""
        self.duration = duration
        """Duration in milliseconds."""
        self.parent = parent
        """Sequence, if any, that this subtitle belongs to."""
        self.index = index
        """Index number if part of a sequence."""
        self.next = next
        """Next subtitle if part of a sequence."""
        self.previous = previous
        """Previous subtitle if part of a sequence."""

    def __iter__(self):
        yield from self.lines

    def __len__(self):
        return len(self.plain)

    def __contains__(self, text):
        if isinstance(text, str):
            return any(text in line for line in self)
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Subtitle):
            return self.lines == other.lines
        elif isinstance(other, list):
            return self.lines == other
        elif isinstance(other, str):
            return '\n'.join(self.lines) == other
        else:
            return NotImplemented

    def __str__(self):
        return '|'.join(self.lines)

    def __repr__(self):
        klass = self.__class__.__name__
        start = self.start_time
        end   = self.end_time
        lines = ', '.join(f'"{line}"' for line in self.lines)
        return f'{klass}({start} → {end}: {lines})'

    @property
    def prev(self):
        """Alias for `previous`."""
        return self.previous

    @prev.setter
    def prev(self, value):
        self.previous = value

    @property
    def end(self):
        return self.start + self.duration

    @end.setter
    def end(self, value):
        """End time in milliseconds."""
        self.duration = value - self.start

    @property
    def start_time(self):
        """Start time in time-stamp format `hh:mm:ss.ms`."""
        return timestamp.format(self.start)

    @start_time.setter
    def start_time(self, value):
        self.start = timestamp.parse(value)

    @property
    def end_time(self):
        """End time in time-stamp format `hh:mm:ss.ms`."""
        return timestamp.format(self.end)

    @end_time.setter
    def end_time(self, value):
        self.end = timestamp.parse(value)

    @property
    def text(self):
        """The entire text of the subtitle, all lines joined together."""
        return '\n'.join(self.lines)

    @text.setter
    def text(self, value):
        self.lines = value.strip().splitlines()

    @property
    def plain(self):
        """The entire text, but any markup removed."""
        return re.sub(r'<.*?>', '', self.text)
