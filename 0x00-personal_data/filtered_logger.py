#!/usr/bin/env python3
'''The module implements logger that filters out PII data out'''
import logging
import re
from typing import List, Union
from os import getenv

from mysql.connector.connection import MySQLConnection
import mysql.connector  # type: ignore

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


class RedactingFormatter(logging.Formatter):
    '''Redacting Formatter class'''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''The method filters out the values of "self.fields" in the incoming
        log records using the helper function "filter_datum"'''
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    '''The function returns <logging.Logger> object named "user_data"'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    '''The function creates and returns a connector to the database,
    using values from enviroment variables'''
    params = {
        "user": getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        "host": getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        "database": getenv("PERSONAL_DATA_DB_NAME", "")
    }

    # return mysql.connector.connect(**params)
    # return MySQLConnection(**params)
    return MySQLConnection(user=params["user"], password=params["password"],
                           host=params["host"], database=params["database"])


def main():
    '''Entry point
    retrieve all rows in the "users" table in the database and display each
    row under a filtered format'''
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    cols = [column[0] for column in cursor.description]

    for row in cursor:
        row = map(lambda i: str(i), row)
        msg = "; ".join(["=".join(field) for field in list(zip(cols, row))])
        if len(msg):
            msg += ";"
        logger.info(msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
