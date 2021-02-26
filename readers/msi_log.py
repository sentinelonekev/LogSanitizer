from .reader import MultiLineReader


LEADER = r"^=== \w+ logging started:.+msiexec\.exe ==="

FIELDS = r"""
(?P<Prefix>^
    MSI \(c\) \([A-F0-9]{2}:[A-F0-9]{2}\) \[\d{2}:\d{2}:\d{2}:\d{3}\]:
)
(?P<Text>.+)
"""

class MsiLogFile(MultiLineReader):
    """
    S1 Windows MSI log file
    """

    def __init__(self):
        super().__init__(LEADER, FIELDS)

    @property
    def description(self):
        return "MSI Installer log file."

