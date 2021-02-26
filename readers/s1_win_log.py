from .reader import MultiLineReader

"""
S1 parsed Windows log file
"""

LEADER = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"

FIELDS = r"""
    (?P<Prefix>^
        (?P<Timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?)\s+
        (?P<PID>\d+)\s+
        (?P<TID>\d+)\s+
        (?P<File>\w+\.\w+)\s+
        (?P<Line>\d+)\s+
        (?P<Level>\w+)\s+
    )
    (?P<Text>.+)
"""

class S1WinLogFile(MultiLineReader):
    def __init__(self):
        super().__init__(LEADER, FIELDS)

    @property
    def description(self):
        return "S1 Windows parsed BinLog file."
