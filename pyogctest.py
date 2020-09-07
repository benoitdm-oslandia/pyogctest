#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"

import os
import datetime
import argparse

from pyogctest.logger import Logger
from pyogctest.report.format import Format
from pyogctest.report.report import Report
from pyogctest.teamengine import Teamengine


if __name__ == "__main__":
    # aprse args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        type=str,
        help="URL",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Docker container binding port (default: '8081')",
        default=8081,
    )

    parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")

    parser.add_argument(
        "-x", "--xml", help="Save Teamengine XML report", action="store_true"
    )

    parser.add_argument(
        "-f",
        "--format",
        help="Output format (default: 'prompt')",
        type=Format,
        choices=list(Format),
        default=Format.PROMPT,
    )

    parser.add_argument(
        "-s",
        "--suite",
        help="Test suite (default: 'wms130')",
        type=Teamengine.TestSuite,
        choices=list(Teamengine.TestSuite),
        default=Teamengine.TestSuite.WMS130,
    )

    # promp format parameters
    parser.add_argument(
        "-r",
        "--regex",
        help="Regular expression. Only the 'prompt' format is affected by this option",
        type=str,
        default="",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose mode. Only the 'prompt' format is affected by this option",
        action="store_true",
    )

    # html format parameters
    pwd = os.path.dirname(os.path.realpath(__file__))
    help_str = "Output directory. Only the 'html' format is affected by this option (default: '{}/teamengine')".format(
        pwd
    )
    parser.add_argument(
        "-o",
        "--output",
        help=help_str,
        type=str,
        default=os.path.join(pwd, "teamengine"),
    )

    parser.add_argument(
        "-c",
        "--commit",
        help="QGIS commit number. Only the 'html' format is affected by this option (default: None)",
        type=str,
        default="",
    )

    parser.add_argument(
        "-b",
        "--branch",
        help="QGIS branch name. Only the 'html' format is affected by this option (default: 'master')",
        type=str,
        default="master",
    )
    args = parser.parse_args()

    # init logging
    Logger.init(args.debug)
    Logger.log(" OGC test session starts ", center=True, symbol="=")

    if args.suite == Teamengine.TestSuite.WMS130:
        Logger.log("testsuite: WMS 1.3.0")

    # run OGC tests with Teamengine
    start = datetime.datetime.now()
    # t = Teamengine(args.suite, args.port)

    Logger.debug("Pull docker image")
    # t.pull()

    Logger.debug("Start container")
    # t.start()

    Logger.debug("Run OGC tests")
    # xml = t.run(args.url)
    # t.stop()
    end = datetime.datetime.now()

    if args.xml:
        with open("teamengine.xml", "r") as f:
            # f.write(xml)
            xml = f.read()

    # parse xml report
    Logger.debug("Parse XML report")
    r = Report(args.suite, xml, (end - start).seconds)
    r.dump(args.verbose, args.regex, args.format, args.output, args.commit, args.branch)
