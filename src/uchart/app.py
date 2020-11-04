#!/usr/bin/env python
"""
Module that contains the command line app.

"""
import argparse
import logging
import os
import sys
import csv
import traceback

def main():
    """
        The main function that operates as a wrapper around jwpi.
    """
    print("Uchart main")
    try:
        sys.exit()
    except Exception as err:
        logging.error('%s', err)
        traceback.print_exc()
        sys.exit(1)
