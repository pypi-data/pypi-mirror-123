"""Import subtitles from various file formats."""

from .subtitle import Subtitle
from .subtitles import Subtitles
from . import formats

import srt
import aeidon
import chardet
from pathlib import Path


def detect_encoding(file):
    """
    Detects the text encoding of the given `file`.

    Reads the file line by line and passes each line to the detector
    provided by the [Chardet][chardet] library, which will usually
    recognize the encoding correctly based on the file's content.

    [chardet]: https://pypi.org/project/chardet
    """
    detector = chardet.universaldetector.UniversalDetector()
    with file.open('rb') as stream:
        for line in stream:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    encoding = detector.result['encoding']
    rename = {
        'utf-8':        'UTF-8',
        'UTF-8-SIG':    'UTF-8-sig',
    }
    if encoding in rename:
        encoding = rename[encoding]
    return encoding


def from_aeidon(aeidon_subtitles, markup):
    """Convert subtitles from Aeidon's format to the internal one."""
    subtitles = []
    for sub in aeidon_subtitles:
        subtitle = Subtitle()
        subtitle.text  = markup.convert(sub.main_text)
        subtitle.start = round(1000 * sub.start_seconds)
        subtitle.end   = round(1000 * sub.end_seconds)
        subtitles.append(subtitle)
    return subtitles


def read_srt(file, encoding):
    """Reader for SubRip (.srt) subtitle files."""
    content   = file.read_text(encoding=encoding)
    srt_subs  = list(srt.parse(content))
    subtitles = []
    for sub in srt_subs:
        lines = sub.content.splitlines()
        start = round(sub.start.total_seconds() * 1000)
        end   = round(sub.end.total_seconds() * 1000)
        subtitles.append(Subtitle(lines, start, end-start))
    source = {'file': file, 'encoding': encoding}
    return Subtitles(subtitles, source)


def read_ass(file, encoding):
    """Reader for Advanced Substation Alpha (.ass) subtitle files."""
    reader = aeidon.files.AdvSubStationAlpha(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.ASS, aeidon.formats.SUBRIP)
    source = {'file': file, 'encoding': encoding}
    return Subtitles(from_aeidon(reader.read(), markup), source)


def read_ssa(file, encoding):
    """Reader for Substation Alpha (.ssa) subtitle files."""
    reader = aeidon.files.SubStationAlpha(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SSA, aeidon.formats.SUBRIP)
    source = {'file': file, 'encoding': encoding}
    return Subtitles(from_aeidon(reader.read(), markup), source)


def read_vtt(file, encoding):
    """Reader for Web Video Text Tracks (.vtt) subtitle files."""
    reader = aeidon.files.WebVTT(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.WEBVTT,
                                    aeidon.formats.SUBRIP)
    source = {'file': file, 'encoding': encoding}
    return Subtitles(from_aeidon(reader.read(), markup), source)


def read_sub(file, encoding):
    """Reader for SubViewer 2.0 (.sub) subtitle files."""
    reader = aeidon.files.SubViewer2(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SUBVIEWER2,
                                    aeidon.formats.SUBRIP)
    source = {'file': file, 'encoding': encoding}
    return Subtitles(from_aeidon(reader.read(), markup), source)


readers = {
    'SubRip':    read_srt,
    'ASS':       read_ass,
    'SSA':       read_ssa,
    'WebVTT':    read_vtt,
    'SubViewer': read_sub,
}


def load(file, format=None, encoding=None):
    """
    Loads subtitles from a file.

    `file` is preferably a `pathlib.Path` object, but may also be a
    string denoting an absolute or relative file path.

    The file `format`, if not explicitly specified, is deduced from the
    file ending. The file's text `encoding` can be given, but is otherwise
    detected automatically (which may fail in some rare cases).

    Returns a `Subtitles` object.
    """
    file = Path(file)
    if format is None:
        suffix = file.suffix.lower()
        if suffix in formats:
            format = formats[suffix]
        else:
            raise ValueError(f'Unknown file ending "{suffix}".')
    if format in readers:
        reader = readers[format]
    else:
        raise ValueError(f'No reader for subtitles format "{format}".')
    if not encoding:
        encoding = detect_encoding(file)
    return reader(file, encoding)


read = load
"""Alias for `load()`."""
