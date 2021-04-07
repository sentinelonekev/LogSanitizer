from pathlib import Path
from glob import glob
from logging import basicConfig, critical as CRITICAL, debug as DEBUG, error as ERROR, fatal as FATAL, info as INFO, log as LOG

from readers import MsiLogFile, S1BinLogFile, S1LinuxLogFile, S1LinuxInstallerLogFile, S1OsxLogFile, S1WinLogFile, Reader
from cui import Cui_Filenames, Cui_Guids, Cui_Md5s, Cui_Sha1s, Cui_Sha256s, Cui_Ipv4s, Cui_Ipv6s, Cui_Urls

class LogSanitizer():
    """
        Generic File Sanitizer
    """
    def __init__(self):
        self.readers = [
            MsiLogFile(),
            S1BinLogFile(),
            S1WinLogFile(),
            S1LinuxLogFile(),
            S1LinuxInstallerLogFile(),
            S1OsxLogFile()
        ]

        self.CUIs = [
            Cui_Filenames(),
            Cui_Md5s(),
            Cui_Sha1s(),
            Cui_Sha256s(),
            Cui_Ipv4s(),
            # Cui_Ipv6s(),
            Cui_Guids(),
            Cui_Urls(),
            # Cui_Emails()
        ]

        self.filenames = []

    # --------------------------------------------------------------------------

    def sanitize_files(self, args: object) -> None:
        '''
            Sanitize files listed on command-line

            args: parsed command-line arguments

        '''
        for name in args.files:
            for filename in glob(name):
                DEBUG(f"Filename: {filename}")

                for reader in self.readers:
                    if reader.detect(filename):
                        DEBUG(f"reader: {reader.__class__.__name__}")

                        message = f"{filename} - {reader.description}"
                        self.filenames.append(message)
                        print(message)

                        self.make_target_dir(args.out)

                        self.sanitize_file(filename, args.out, reader)
                        break
                else:
                    print(f"No handler found for {filename}.")

    # --------------------------------------------------------------------------
    """
    create target directory -if it doesn't exist
    """
    @staticmethod
    def make_target_dir(filename: str):
        if not filename:
            return

        target = Path(filename)

        if target.exists() and not target.is_dir():
            raise Exception(f"{target} is not a valid path.")
        else:
            target.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------

    def timings(self) -> None:
        '''
            Print Timing results
        '''

        print("Timings")
        print("=======")

        total = 0.0

        for cui in self.CUIs:
            print(f"{__class__.__name__}: {cui.time}")
            total += cui.time

        print(f"\nTotal: {total}")

    # --------------------------------------------------------------------------
    '''
        Create Secret Translation file
    '''
    def save_secrets(self, out: str, version: str) -> None:
        with open("secret_translation_file.txt", "w", encoding="utf-8") as file:
            file.write(f"Sanitized Translation Keys\n{26*'='}\nv{version}\n")

            file.write("Input Logs\n==========\n")

            for filename in self.filenames:
                file.write(f"{filename}\n")

            file.write("\n")

            for cui in self.CUIs:
                cui.save(file)

    # --------------------------------------------------------------------------
    '''
        Create sanitized file

            filename: file to sanitize
            out: optional output directory
            reader: file reader to iterate lines
    '''
    def sanitize_file(self, filename: str, out: str, reader: Reader) -> None:
        path = Path(filename)

        if out:
            target = path.parent / out / path.with_name(f"SANITIZED_{path.name}")
        else:
            target = path.parent / path.with_name(f"SANITIZED_{path.name}")
        DEBUG(f"Target: {target}")

        with open(target, "w", encoding="utf-8") as file:
            for i, line in enumerate(reader.lines(filename), start=1):
                DEBUG(f"{i}: {line.prefix}{line.text}")
                sanitized = self.sanitize_line(line.text)
                file.write(f"{line.prefix}{sanitized}")

    # --------------------------------------------------------------------------
    '''
        Sanitize a line of text
    '''
    def sanitize_line(self, line: str) -> str:
        DEBUG(line.rstrip())

        for cui in self.CUIs:
            DEBUG(f"CUI: {__class__.__name__}")
            line = cui.sanitize(line)

        DEBUG(f"-> {line}")
        return line

