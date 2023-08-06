"""Export subtitles to various file formats."""

from . import formats
from . import timestamp

import aeidon
from pathlib import Path


def to_aeidon(subtitles, markup):
    """Convert subtitles from the internal format to Aeidon's."""
    aeidon_subtitles = []
    for subtitle in subtitles:
        new = aeidon.Subtitle()
        new.main_text     = markup.convert(subtitle.text)
        new.start_seconds = subtitle.start / 1000
        new.end_seconds   = subtitle.end / 1000
        aeidon_subtitles.append(new)
    return aeidon_subtitles


def write_srt(subtitles, file, encoding):
    """Writer for SubRip (.srt) subtitle files."""
    with file.open('w', encoding=encoding) as stream:
        for (index, subtitle) in enumerate(subtitles):
            start = timestamp.format(subtitle.start, format='SubRip')
            end   = timestamp.format(subtitle.end, format='SubRip')
            stream.write(f'{index+1}\n')
            stream.write(f'{start} --> {end}\n')
            stream.write(subtitle.text + '\n')
            if subtitle.next:
                stream.write('\n')


def write_ass(subtitles, file, encoding):
    """Writer for Advanced Substation Alpha (.ass) subtitle files."""
    writer = aeidon.files.AdvSubStationAlpha(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SUBRIP, aeidon.formats.ASS)
    writer.write(to_aeidon(subtitles, markup), aeidon.documents.MAIN)


def write_ssa(subtitles, file, encoding):
    """Writer for Substation Alpha (.ssa) subtitle files."""
    writer = aeidon.files.SubStationAlpha(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SUBRIP, aeidon.formats.SSA)
    writer.write(to_aeidon(subtitles, markup), aeidon.documents.MAIN)


def write_vtt(subtitles, file, encoding):
    """Writer for Web Video Text Tracks (.vtt) subtitle files."""
    writer = aeidon.files.WebVTT(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SUBRIP,
                                    aeidon.formats.WEBVTT)
    writer.write(to_aeidon(subtitles, markup), aeidon.documents.MAIN)


def write_sub(subtitles, file, encoding):
    """Writer for SubViewer 2.0 (.sub) subtitle files."""
    writer = aeidon.files.SubViewer2(file, encoding)
    markup = aeidon.MarkupConverter(aeidon.formats.SUBRIP,
                                    aeidon.formats.SUBVIEWER2)
    writer.write(to_aeidon(subtitles, markup), aeidon.documents.MAIN)


writers = {
    'SubRip':    write_srt,
    'ASS':       write_ass,
    'SSA':       write_ssa,
    'WebVTT':    write_vtt,
    'SubViewer': write_sub,
}


def save(subtitles, file, encoding=None, format=None):
    """
    Saves subtitles to a file.

    A `file` must be specified, preferably as a `Path` object, or as a
    string denoting a path includinf the file name. Exisiting files
    will be overwritten.

    If no `encoding` is given, it defaults to `UTF-8-sig', that is,
    variable-length Unicode with signature / byte-order mark.

    A `format` such as `'SubRip'` can be enforced, otherwise it will be
    chosen in accordance with the given file's ending, e.g. `.srt`.
    Valid file endings and formats are those returned by `subsy.formats`.
    """
    file = Path(file)
    if not encoding:
        encoding = 'UTF-8-sig'
    if not format:
        suffix = file.suffix.lower()
        if suffix in formats:
            format = formats[suffix]
        else:
            raise ValueError(f'Unknown file ending "{suffix}".')
    if format in writers:
        writer = writers[format]
    else:
        raise ValueError(f'No writer for subtitles format "{format}".')
    return writer(subtitles, file, encoding)


write = save
"""Alias for `save()`."""
