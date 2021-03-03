# SentinelOne Log Sanitizer
## Objective

The Log Sanitizer is intended to replace all Customer User Information (**CUI**) from log files with data that is logically consistent, yet however, contains no identifiable information.

For Example: all references to "*Secret File.Doc*" could be replaced with "Filename_0001" in a "SANITIZED" version of the log file.  This new file could be distributed to Technical Staff that are unauthorized to see the original file names.

python -m pip install -r requirements.txt

