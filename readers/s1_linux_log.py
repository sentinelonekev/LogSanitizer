from .reader import MultiLineReader

"""
S1 Linux log file
"""

LEADER = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\]"

FIELDS = r"""
    (?P<Prefix>^
        (?P<Timestamp>\[\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}\.\d{6}\])\s+
        (?P<PID>\[\d+\])\s+
        (?P<Level>\[\w+\])\s+
        (?P<Detector>
            \[detector\]\s+
            (?P<File>\[\w+\.\w+\])\s+
        )?
    )
    (?P<Text>.+)
"""

class S1LinuxLogFile(MultiLineReader):
    def __init__(self):
        super().__init__(LEADER, FIELDS)

    @property
    def description(self):
        return "S1 Linux Log file."
