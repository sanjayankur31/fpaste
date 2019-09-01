#!/usr/bin/env python3
"""
Logger for fpaste.

File: logger.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import logging


def get_module_logger(module_name="fpaste", logging_level=logging.DEBUG):
    """Get a logger for the module.

    :module_name: name of the module
    :logging_level: logging level
    :returns: created logger

    """
    lgr = logging.getLogger(module_name)
    lgr.setLevel(logging_level)
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    formatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    lgr.addHandler(handler)

    return lgr
