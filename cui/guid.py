from re import Match

from .cui import Cui
from .storage import Guid

'''-----------------------------------------------------------------------------
    GUIDs
    =====
    12345678-1234-ABCD-EFFF-0123456789AB
'''

class Cui_Guids(Cui):
    def __init__(self) -> None:
        super().__init__(
            title="Guids",
            regex=r"(?im)(?<![a-z0-9])[{(]?(?P<guid>[0-9A-F]{8}[-](?:[0-9A-F]{4}[-]){3}[0-9A-F]{12})[)}]?(?![a-z0-9])",
            value=Guid()
        )

    def key_from_match(self, m: Match) -> str:
        return m['guid']
