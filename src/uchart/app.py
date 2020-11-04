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

try:
    import colorlog
    HAVE_COLORLOG = True
except ImportError:
    HAVE_COLORLOG = False

from . import __version__
from .libuchart import (uchart_plugin)
from . import filter

LOGO = r'''
  _    _    _____   _    _              _____    _______
 | |  | |  / ____| | |  | |     /\     |  __ \  |__   __|
 | |  | | | |      | |__| |    /  \    | |__) |    | |
 | |  | | | |      |  __  |   / /\ \   |  _  /     | |
 | |__| | | |____  | |  | |  / ____ \  | | \ \     | |
  \____/   \_____| |_|  |_| /_/    \_\ |_|  \_\    |_|
 '''


def set_level_debug():
    logging.getLogger().setLevel(logging.DEBUG)


def set_level_info():
    logging.getLogger().setLevel(logging.INFO)


def create_logger():
    """
        Setup the logging environment
    """
    log = logging.getLogger()  # root logger
    log.setLevel(logging.INFO)
    format_str = "%(asctime)s %(levelname)s [%(module)s:%(funcName)s] %(message)s"
    date_format = '%d-%b-%y %H:%M:%S'
    if HAVE_COLORLOG:
        cformat = '%(log_color)s' + format_str
        colors = {'DEBUG': 'bold_cyan',
                  'INFO': 'bold_green',
                  'WARNING': 'bold_yellow',
                  'ERROR': 'bold_red',
                  'CRITICAL': 'bold_red'}
        formatter = colorlog.ColoredFormatter(
            cformat, date_format, log_colors=colors)
    else:
        formatter = logging.Formatter(format_str, date_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return logging.getLogger(__name__)


def uchart_get_argparser():
    """
        Creates an argparser for kas with all plugins.
    """
    parser = argparse.ArgumentParser(
        prog="uchart",
        description="Command line application for managing JRC user maps"
    )

    verstr = f'%(prog)s {__version__}'

    parser.add_argument('-V', '--version', action='version', version=verstr)

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help="display verbose debug messages")

    subparser = parser.add_subparsers(help='sub command help', dest='cmd')

    for plugin in getattr(uchart_plugin, 'plugins', []):
        plugin.get_argparser(subparser)

    return parser


def uchart(argv):
    logger = create_logger()

    is_python3_6 = sys.version_info.major == 3 and sys.version_info.minor >= 6
    if not is_python3_6:
        logger.critical("Required version of python is 3.6+ but "
                        f"{sys.version_info.major}.{sys.version_info.minor} was found!")
        sys.exit()
    parser = uchart_get_argparser()
    args = parser.parse_args(argv)

    if args.debug:
        set_level_debug()

    logger.info(LOGO)
    logger.info('%s %s started', os.path.basename(sys.argv[0]), __version__)

    for plugin in getattr(uchart_plugin, 'plugins', []):
        if plugin().run(args):
            return

    parser.print_help()
    print()


def main():
    """
        The main function that operates as a wrapper around uchart.
    """
    try:

        print(str(sys.argv))
        sys.exit(uchart(sys.argv[1:]))
    except Exception as err:
        logging.error('%s', err)
        traceback.print_exc()
        sys.exit(1)
