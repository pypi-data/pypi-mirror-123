from .meta import version as __version__
from .meta import synopsis as __doc__

formats = {
    '.srt': 'SubRip',
    '.ass': 'ASS',
    '.ssa': 'SSA',
    '.vtt': 'WebVTT',
    '.sub': 'SubViewer',
}

from .readers   import load
from .subtitles import Subtitles
from .subtitle  import Subtitle
