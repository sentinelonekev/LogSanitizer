from re import compile, fullmatch, Match

from .cui import Cui
from .storage import Bytes

# ==============================================================================
'''
    Filenames
    =========
    C:\\Path\\Name.Ext
    \\Device\\HarddiskVolumeX\\Path\\Name.Ext
    "C:\\Path with spaces\\Name.Ext"
    "\\Device\\HarddiskVolumeX\\Path with spaces\\Name.Ext"
'''

class Cui_Filenames(Cui):
    def __init__(self) -> None:
        super().__init__(
            title="Filenames",
            regex=[
                r"""
                (?im)
                (?P<fullname>
                    (?P<path>
                        (?P<drive>([a-z]:|\\{1,2}Device\\{1,2}HarddiskVolume\d)\\{1,2})
                        (?P<folder>[\w\ \.]*\\{1,2})*
                    )?
                    (?P<filename>
                        (?P<name>([\w\ ]*))
                        \.
                        (?P<extension>(exe|sys|drv|json|dll))
                    )
                )
                """,
                r"""
                (?im)
                (?P<quote1>\")?
                (?P<fullname>
                    (?P<path>
                        (?P<drive>([a-z]:|\\{1,2}Device\\{1,2}HarddiskVolume\d)\\{1,2})
                        (?P<folder>((?(quote1)[\w\ \.]|[\w\.])*\\{1,2}))*
                    )?
                    (?P<filename>
                        (?P<name>(?(quote1)[\w\ ]|[\w])*)
                        \.
                        (?P<extension>(?(quote1)[\w\ ]|[\w])*)
                    )
                )
                (?P<quote2>(?(quote1)\"|))
                """
            ],
            value=Bytes(4)
        )

    # --------------------------------------------------------------------------
    '''
    Override to allow further rejection of matched data
    '''
    ALL_NUMERIC = compile(r"\d*\.?\d*")
    LAST_WORD = compile(r"[a-zA-z]+\.")

    def reject(self, m: Match) -> bool:
        return any(fullmatch(pattern, m['filename'])
            for pattern in
            [
                self.ALL_NUMERIC,
                self.LAST_WORD
            ])

    # --------------------------------------------------------------------------
    '''
    Returns current value as a string
    found: text to replace
    '''
    def replacement(self, found: str) -> str:
        return f"Filename_{int.from_bytes(self.value.bytes, 'big'):05d}"
        # {Path(found).suffix}
