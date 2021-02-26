from collections.abc import Iterable

from .reader import Reader, LineTuple

"""
S1 Windows BinLog file.
"""

LEADER = b'\xa3\x58\x49\xd3'

class S1BinLogFile(Reader):
    def __init__(self):
        super().__init__(LEADER)

    @property
    def description(self):
        return "S1 Windows BinLog file (unparsed)."

    '''
        Iterate through :filename: returning LineTuples consisting of a:
            prefix: string at beginning of line that has no CUI
            text: rest of the line that needs sanitizing
    '''
    def lines(self, filename: str) -> Iterable[LineTuple]:
        pass
