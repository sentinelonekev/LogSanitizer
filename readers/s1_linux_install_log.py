from .reader import MultiLineReader

"""
S1 Linux Installer log file
"""

LEADER = r"^\[\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\]"

FIELDS = r"""
    (?P<Prefix>^
        (?P<Timestamp>\[\d{2}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2}\.\d{3}\])\s+
    )
    (?P<Text>.+)
"""

class S1LinuxInstallerLogFile(MultiLineReader):
    def __init__(self):
        super().__init__(LEADER, FIELDS)

    @property
    def description(self):
        return "S1 Linux Installer Log file."
