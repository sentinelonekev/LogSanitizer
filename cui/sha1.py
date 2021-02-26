from .cui import Cui
from .storage import Bytes

'''-----------------------------------------------------------------------------
    SHA1s
    =====
    1234567890123456789012345678901234567890
'''

class Cui_Sha1s(Cui):
    def __init__(self):
        super().__init__(
            title="SHA1s",
            regex=r"(?im)(?<![a-z0-9])(?P<sha1>[A-F\d]{40})(?![a-z0-9])",
            value=Bytes(40)
        )
