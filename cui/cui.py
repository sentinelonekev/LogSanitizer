from ipaddress import IPv4Address, IPv6Address
from logging import debug as DEBUG
from pathlib import Path
from re import compile, fullmatch, search, Match, DOTALL, VERBOSE
from timeit import default_timer as timer

from .storage import Bytes, Guid, Incremental, digits

# ==============================================================================
'''
    Base class for all CUI (Confidential User Info)

    title: Report section title
    regex: Regex value to find in a line
    value: Incremented value assigned to all new regex matches
    data: Dictionary to store regex matches and replacement values
    time: Time spent in sanitize() function
'''
class Cui():
    '''
    title: Output message
    regex: Matching regex expression
    '''
    def __init__(self, title: str, regex: [str|list[str]], value: Incremental) -> None:
        self.title = title

        if not isinstance(regex, list):
            regex = [ regex ]

        self.regex = [ compile(x, VERBOSE | DOTALL) for x in regex ]
        self.value = value
        self.data = {}
        self.time = 0

    # --------------------------------------------------------------------------
    '''
    Return a replacement of all regex's with pseudo-values

    text: input text
    return: sanitized line
    '''
    def sanitize(self, text: str) -> str:
        start = timer()
        parts = []

        while m := self.find_in_line(text):
            DEBUG(text)

            key = self.key_from_match(m)

            if self.reject(m):
                value = key
            else:
                if key not in self.data:
                    self.value.increment()
                    self.data[key] = self.replacement(key)

                value = self.data[key]

            offset = text.find(key)
            parts.append(text[:offset])
            parts.append(value)

            text = text[offset + len(key):]

        parts.append(text)
        value = ''.join(parts)

        self.time += timer() - start
        return value

    # --------------------------------------------------------------------------
    '''
    Override to allow further rejection of matched data
    '''
    def reject(self, m: Match) -> bool:
        return False

    # --------------------------------------------------------------------------
    '''
    Returns key from match.  Override for granular key from regex.
    '''
    def key_from_match(self, m: Match) -> str:
        return m[0]

    # --------------------------------------------------------------------------
    '''
    Look for a Match in the line of text.  Override for complex searches.
    '''
    def find_in_line(self, text) -> Match:
        for re in self.regex:
            if found := search(re, text):
                return found

    # --------------------------------------------------------------------------
    '''
    Returns current value as a string
    found: text to replace

    Overridden in derived classes
    '''
    def replacement(self, found: str) -> str:
        return str(self.value)

    # --------------------------------------------------------------------------
    '''
    Saves secret conversion table
    '''
    def save(self, file: object) -> None:
        file.write(f"{self.title}\n{len(self.title)*'='}\n")

        values = dict(sorted(self.data.items(), key=lambda item: item[1]))
        for key in values.keys():
            file.write(f"{values[key]} : {key}\n")

        file.write("\n")
