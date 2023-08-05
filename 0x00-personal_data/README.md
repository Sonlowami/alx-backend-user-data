# Personal Data

## Introduction
This directory contain python modules that does logging, database access,
and password storage in a way that protects personally identifiable 
information.
For any app that will handle user data, there should be clear policies of
storing that data to prevent unauthorized access to a user's information.

In [filtered logger](./filtered_logger.py), we implement logging with user data anonymization. A typical log message looks like this:
`[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s`

In [encrypt password](./encrypt_password.py), we impliment `hash_password(password: str) -> bytes:` to encrypt the password and `is_valid(hash_password: bytes, password: str) -> bool` to check if the password passed is valid.

A good case to use these is to call `hash_password` before storing into a database, and `is_valid` after retrieving a stored hash from the database and checking them against the user provided password

## Disclaimer

Implementation of all these methods does not verify arguments. If you want to use them, clone this repo, but remember to validate arguments before passing them
