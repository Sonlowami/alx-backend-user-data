#!/usr/bin/env python3
"""Contain a number of methods to deal with anonymizing
personal data"""
import logging
import mysql.connector as connector
import os
from typing import List, Dict
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """replace particular fields in a message with a redaction"""
    for field in fields:
        message = re.sub('{}=[^{}]+'.format(field, separator),
                         '{}={}'.format(field, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields: List[str] = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Log output with anonymised fields"""
        record.msg: str = filter_datum(self.fields, self.REDACTION,
                                       record.getMessage(), self.SEPARATOR)
        return super().format(record)


PII_FIELDS: List[str] = ['email', 'phone', 'ssn', 'password', 'name']


def get_logger() -> logging.Logger:
    """Create a logger object with following attributes
        name: user_data
        level: logging.INFO
        propagate: False
        formatter: RedactingFormatter()
        handler: StreamHandler()
    """
    log: logging.Logger = logging.getLogger('user_data')
    log.propagate = False
    log.setLevel(logging.INFO)
    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(handler)
    return log


def get_db() -> connector.MySQLConnection:
    """Create a connection to a mysql database using environment
    variables at the application server"""
    db_config: Dict = {
            'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            'database': os.getenv('PERSONAL_DATA_DB_NAME')
            }
    connection: connector.MySQLConnection = connector.connect(**db_config)
    return connection


def main() -> None:
    """fetch all rows and display each row in a filtered format,
    not revealing sensitive information of the user"""
    log: logging.Logger = get_logger()
    db: connector.MySQLConnection = get_db()
    cursor: connector.cursor.MySQLCursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    message: str = 'name={}; email={}; phone={}; '
    message += 'ssn={}; password={}; ip={}; last_login={}; user_agent={};'
    for row in cursor.fetchall():
        log.info(message.format(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7]))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
