from .cui import Cui
from .storage import Bytes

'''-----------------------------------------------------------------------------
    MD5s
    ====
    12345678901234567890123456789012
'''

class Cui_Md5s(Cui):
    def __init__(self) -> None:
        super().__init__(
            title="MD5s",
            regex=r"(?im)(?<![a-z0-9])(?P<md5>[A-F0-9]{32})(?![a-z0-9])",
            value=Bytes(32)
        )
