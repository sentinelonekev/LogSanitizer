from .cui import Cui
from .storage import Bytes

'''-----------------------------------------------------------------------------
    SHA256s
    =======
    1234567890123456789012345678901234567890123456789012345678901234
'''

class Cui_Sha256s(Cui):
    def __init__(self):
        super().__init__(
            title="SHA256s",
            regex=r"(?im)(?<![a-z0-9])(?P<sha256>[A-F\d]{64})(?![a-z0-9])",
            value=Bytes(64)
        )
