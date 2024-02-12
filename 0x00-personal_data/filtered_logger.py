#!/usr/bin/env python3
"""
function that returns the log message obfuscated
Arguments:

    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is
    separating all fields in the log line (message)
uses a regex to replace occurrences of certain field values.
"""


import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    return the log message obfuscated
    """
    for field in fields:
        msg_obfuscated = re.sub(field + "=.+?" + separator,
                                field + "=" + redaction + separator,
                                message)

   return msg_obfuscated
