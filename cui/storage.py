from abc import ABC, abstractmethod
from math import log10
from uuid import UUID


''' Calculate width of count items '''
def digits(value):
    return int(log10(value) if value else 0) + 1

# ==============================================================================
'''
    Incremental class - must be able to be incremented
'''

class Incremental(ABC):
    @abstractmethod
    def increment(self):
        pass

# ==============================================================================
'''
    Manage an array of bytes and support incrementing them as a ultra-wide value
'''
class Bytes(Incremental):
    ''' size: number of digits (nibbles) '''
    def __init__(self, size: int) -> None:
        self.data = bytearray(size // 2)

    ''' Convert to string '''
    def __str__(self) -> str:
        return ''.join(f"{x:02x}" for x in self.data)

    ''' Increment the ultra-wide value '''
    def increment(self) -> None:
        for i in range(len(self.data) - 1, 0, -1):
            self.data[i] = (self.data[i] + 1) & 0xff

            if self.data[i]:
                return

    ''' syntax sugar helper '''
    @property
    def bytes(self) -> bytes:
        return bytes(self.data)

# ==============================================================================
'''
    Manage Bytes as a GUID
'''
class Guid(Bytes):
    def __init__(self) -> None:
        super().__init__(32)

    def __str__(self) -> str:
        return str(UUID(bytes=bytes(self.data)))

# ==============================================================================

def test_Bytes() -> None:
    value = Bytes(8)

    for _ in range(300):
        print(value)
        value.increment()

# ==============================================================================

def test_Guid() -> None:
    guid = Guid()

    for _ in range(300):
        print(guid)
        guid.increment()

# ==============================================================================

if __name__ == "__main__":
    test_Bytes()
    test_Guid()
