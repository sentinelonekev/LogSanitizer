from argparse import ArgumentParser
from traceback import print_exc
from logging import basicConfig, Formatter, critical as CRITICAL, debug as DEBUG, error as ERROR, fatal as FATAL, info as INFO, log as LOG

from log_sanitizer import LogSanitizer

__version__ = '0.1.0'

#===============================================================================
'''
    Parse the command line
'''
def parse():
    parser = ArgumentParser()

    parser.add_argument('-t', "--time", action="store_true", help="Print timer metrics.")
    parser.add_argument("-l", "--log", dest="logLevel", choices=[ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ],
                    help="Set the logging level (default: %(default)s).", default='INFO')
    parser.add_argument('-o', '--out', help='Optional output folder')
    parser.add_argument('files', nargs='*', metavar="FILE", help='Files to parse.  Wildcards accepted.')

    args = parser.parse_args()

    if len(args.files) == 0:
        raise Exception("No files to parse.")
        # args.files = [ '*.log', '*.binlog' ]

    return args

#===============================================================================
'''
    Main Algorithm
'''
def main():
    args = parse()

    basicConfig(level=args.logLevel, format='%(message)s')

    print(f"SentinelOne Log Sanitizer v{__version__}")

    sanitizer = LogSanitizer()
    sanitizer.sanitize_files(args)
    sanitizer.save_secrets(args.out, __version__)

    if args.time:
        sanitizer.timings()

#===============================================================================

# LINE = "Failed opening persistent JSON file C:\Program Files\SentinelOne\Sentinel Agent 4.3.2.86\config\LocationEngineState.json with error 2"
LINE = "Starting loop sentinel::ResourceMonitor::{ctor}::<lambda_3>::operator ()"

def test():
    sanitizer = LogSanitizer()
    output = sanitizer.sanitize_line(LINE)
    print(output)

#===============================================================================

if __name__ == "__main__":
    try:
        # test()
        main()
    except Exception as e:
        print_exc()

    INFO("Done.")
