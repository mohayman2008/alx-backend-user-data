#!/usr/bin/env python3
'''The module implements logger that filters out PII data out'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''The function obfuscated the "fields" data in a log record "message"
    where all the fields are separated by "separator", and replace "fields"
    data with "redaction" str, '''
    for field in fields:
        pattern = r"({field}=)[^{separator}]+{separator}"
        pattern = pattern.format(field=field, separator=separator)
        replacement = r"\1{}{}".format(redaction, separator)

        message = re.sub(pattern, replacement, message)
    return message
