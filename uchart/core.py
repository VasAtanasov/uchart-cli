#!/usr/bin/env python

import argparse
import logging
import os
import sys
import csv

from uchart.lib import parse_jan9201_content


def main():
    """
    Entry point for the package, uchart.exe in win and uchart in linux
    :return: None
    """
    
    from uchart import __version__

    parser = argparse.ArgumentParser(
        description="Python command line application for mapping csv files of JRC JAN-7201/9201 user map to JRC "
                    "JAN-901B user map.")

    parser.add_argument("jan9201_user_map", help="Exported csv file user map form JRC JAN-9201 'file_name.csv'",
                        type=str)

    parser.add_argument('--debug', action='store_true', help="Display verbose debug messages")

    parser.add_argument('--version', action="version", version=__version__)

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)

    if not args.jan9201_user_map:
        logging.error(" User-map file is a required argument")
        sys.exit()

    # Initialize logging depending on debug mode
    # if args.debug:
    #     logging.basicConfig(level=logging.DEBUG)
    # else:
    #     logging.basicConfig(level=logging.CR      ITICAL)

    file_name = args.jan9201_user_map

    # Check if the file exists
    logging.debug("[-] Checking if the file exists")
    is_file = os.path.isfile(file_name)
    if not is_file:
        logging.debug("[-] File with the specified name does not exists!")
        sys.exit()

    logging.debug(f"[-] File {file_name} is present!")

    if not file_name.endswith(".csv"):
        logging.debug("[-] File must be with csv extension!")
        sys.exit()

    csv_file = open(file_name)
    logging.debug(f"[-] Reading {file_name}...")
    content = list(csv.reader(csv_file))
    file_name = f"{content[2][0][3:]}.csv"

    print(content)

    uchart_objects = parse_jan9201_content(content[3:])

    for obj in uchart_objects:
        print(obj.content)

