"""Helpers for formatting and parsing time-stamps."""

import re


formats = {
    'default', 'hh:mm:ss.ms',
    'SubRip', 'srt', '.srt', 'hh:mm:ss,ms',
}


def format(milliseconds, format=None):
    (s, ms) = divmod(milliseconds, 1000)
    (h, s)  = divmod(s, 3600)
    (m, s)  = divmod(s, 60)
    if format in (None, 'default', 'hh:mm:ss.ms'):
        return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'
    elif format in ('SubRip', 'srt', '.srt', 'hh:mm:ss,ms'):
        return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
    else:
        raise ValueError(f'Unknown time-stamp format "{format}".')


def parse(text, format=None):
    if format in (None, 'default', 'hh:mm:ss.ms'):
        match = re.match(r'(\d\d):(\d\d):(\d\d).(\d\d\d)', text)
    elif format in ('SubRip', 'srt', '.srt', 'hh:mm:ss,ms'):
        match = re.match(r'(\d\d):(\d\d):(\d\d),(\d\d\d)', text)
    else:
        raise ValueError(f'Unknown time-stamp format "{format}".')
    h  = int(match.group(1))
    m  = int(match.group(2))
    s  = int(match.group(3))
    ms = int(match.group(4))
    return ((h*60 + m)*60 + s)*1000 + ms
