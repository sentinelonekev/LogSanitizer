from .reader import MultiLineReader

"""
S1 OSX log file
"""

LEADER = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}\d{1,2}\s\d{2}:\d{2}:\d{2}"

FIELDS = r"""
(?P<Prefix>^
    (?P<Timestamp>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}\d{1,2}\s\d{2}:\d{2}:\d{2})
    (?P<Id>\w+)\s+
    (?P<Module>[\w\.]+)\[(?P<Line>\d+)\]\s+
)
"""

class S1OsxLogFile(MultiLineReader):
    def __init__(self):
        super().__init__(LEADER, FIELDS)

    @property
    def description(self):
        return "S1 OSX log file."
