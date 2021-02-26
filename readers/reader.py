from abc import abstractmethod, ABC
from chardet import detect
from collections import namedtuple
from collections.abc import Iterable
from re import compile, match, DOTALL, VERBOSE
from typing import TypeVar

# ==============================================================================
'''
    LineTuple:
        prefix: contains no CUI data (date, file names, etc.)
        text: contains CUI data
'''
LineTuple = namedtuple("LineTuple", "prefix text")
T = TypeVar('T')

# ==============================================================================
'''
Base class for reading files
'''
class Reader(ABC):
    def __init__(self, leader: str):
        self.leader = compile(leader)
        self.count = 0

    '''
        Return a human-readable description of the class.
    '''
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    '''
        Return true if this reader supports this filename
    '''
    def detect(self, filename: str) -> bool:
        try:
            with open(filename, "r", encoding=self.encoding(filename)) as file:
                line = file.readline()

                return match(self.leader, line) != None
        except:
            return False

    '''
        Iterate through :filename: returning LineTuples consisting of a:
            prefix: string at beginning of line that has no CUI
            text: rest of the line that needs sanitizing
    '''
    @abstractmethod
    def lines(self, filename: str) -> Iterable[LineTuple]:
        pass

    @staticmethod
    def encoding(filename: str) -> str:
        count = 2000

        with open(filename, "rb") as file:
            rawdata = b''.join(file.readline() for _ in range(count))

        return detect(rawdata)['encoding']

# ==============================================================================
'''
Base class for reading files
'''
class LineReader(Reader):
    def __init__(self, leader: str):
        super().__init__(leader)

    '''
        Iterate through file returning line Tuples
        consisting of a:
            text: rest of the line that needs sanitizing
    '''
    def lines(self, filename: str) -> Iterable[LineTuple]:
        for line in open(filename, "r", encoding=self.encoding(filename)):
            yield line

# ==============================================================================
'''
Base class for reading multi-lined log files.
'''
class MultiLineReader(Reader):
    '''
        leader: Regex found at beginning of each record.
        fields: Regex to split a record into fields.
    '''
    def __init__(self, leader: str, fields: str):
        super().__init__(leader)
        self.fields = compile(fields, DOTALL | VERBOSE)

    '''
        Iterate through file returning line Tuples
        consisting of a:
            prefix: string at beginning of line that has no CUI
            text: rest of the line that needs sanitizing
    '''
    def lines(self, filename: str) -> Iterable[LineTuple]:
        with open(filename, "r", encoding=self.encoding(filename)) as file:
            for line in self.readlines(file):
                m = match(self.fields, line)

                if not m:
                    print(f"Cannot parse this log line:\n{line}\n")
                    continue

                if "DB Stats:" in line:
                    continue

                yield LineTuple(prefix=m['Prefix'], text=m['Text'])

    def readlines(self, file: object) -> str:
        pushback = None
        result = ""

        while True:
            if pushback:
                result = pushback
                pushback = None

            line = file.readline()
            self.count += 1

            if self.count % 1000 == 0:
                print(self.count)

            if not line:
                yield result
                return

            if match(self.leader, line):
                if result:
                    pushback = line
                    yield result
                else:
                    result = line
            else:
                result += line
