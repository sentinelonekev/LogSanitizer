from ipaddress import IPv4Address

from .cui import Cui
from .storage import Bytes

'''-----------------------------------------------------------------------------
    IPv4s
    =====
    255.255.255.255
'''

class Cui_Ipv4s(Cui):
    def __init__(self):
        super().__init__(
            title="IPv4s",
            regex=r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
            value=Bytes(8)
        )

    def replacement(self, found:str) -> str:
        return str(IPv4Address(self.value.bytes))