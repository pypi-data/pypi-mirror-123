#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/globs.py

    Global definitions.

    ___________________________________________________________________________

    o  VERBOSITY_MINIMAL
    o  VERBOSITY_NORMAL
    o  VERBOSITY_DETAILS
    o  VERBOSITY_DEBUG

    o  ARGS

    o  TIMEITNUMBER

    o  TMPFILENAME

    o  REGEX_CMP
    o  REGEX_CMP__HELP

    o  REPORT_SHORTCUTS

    o  DEFAULT_CONFIG_FILENAME
    o  DEFAULTCFGFILE_URL

    o  MODULES

    o  SERIALIZERS

    o  DATA
    o  UNAVAILABLE_DATA

    o  FILECONSOLE_FILEOBJECT
    o  FILECONSOLE

    o  OUTPUT

    o  PROGRESSBAR_LENGTH

    o  UNITS

    o  LOGFILE_NAME
"""
import re


# values defined for --verbosity:
VERBOSITY_MINIMAL = 0
VERBOSITY_NORMAL = 1
VERBOSITY_DETAILS = 2
VERBOSITY_DEBUG = 3

# command line arguments
# will be set to argparse.ArgumentParser(...).parse_args()
ARGS = None

# number of times each serializer is called
TIMEITNUMBER = 1

# temp file default name
TMPFILENAME = "wisteria.tmp"

# regex used to parse the --cmp argument string
REGEX_CMP = re.compile(r"^\s*(?P<serializer1>[^\s\(\)]+)"
                       r"((\svs\s|\sversus\s|\sagainst\s)(?P<serializer2>[^\s\(\)]+))?"
                       r"(\s*\((?P<cmpdata>all|cwc|ini)\))?\s*$")
# string used by --help
REGEX_CMP__HELP = "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

# REPORT_SHORTCUTS has two goals:
# (1) it translates a simple, human-readable string into a list of section parts
# (2) it gives all the accepted keywords that --report may understand.
REPORT_SHORTCUTS = {
    "bestof": "B1c;C2b;C2c;graphs;",
    "full": "titles;A;B;C;D1a;graphs;",
    "full+": "titles;A;B;C;D1b;graphs;",
    "full_debug": "titles;A;B;C;D;graphs;",
    "glance": "titles;B1b;C1a;C1b;C2a;C2b;C2c;graphs;",
    "laconic": "C;graphs;",
    "minimal": "C2c;graphs;",
    "none": "",
    }

# default name for the config file.
DEFAULT_CONFIG_FILENAME = "wisteria.ini"
# url of the default config file:
DEFAULTCFGFILE_URL = "https://raw.githubusercontent.com/suizokukan/wisteria/main/wisteria.ini"

# imported serializers modules
MODULES = {}

# dict storing all serializers used by the program.
#
# * format: SERIALIZERS[(str)serializer name] = SerializerData object
# * initialized by serializers.py::init_serializers()
SERIALIZERS = {}
# dict storing all serializers that the program can't use.
#
# * format: UNAVAILABLE_SERIALIZERS[(str)serializer name] = SerializerData object
# * initialized by serializers.py::init_serializers()
UNAVAILABLE_SERIALIZERS = {}

# dict storing all data used by the program.
#
# * format: DATA[(str)data name] = data object
# * initialized by data.py::init_data()
DATA = {}
# dict storing all data that the program can't use.
#
# * format: UNAVAILABLE_DATA[(str)data name] = string explaining why it's unavailable
# * initialized by data.py::init_data()
UNAVAILABLE_DATA = {}

# log file.
#

# Both variables are initialized by main.py()
FILECONSOLE_FILEOBJECT = None
#   value: rich.console.Console(file=...)
FILECONSOLE = None

# value of the --output argument
#  initialized by parse_output_argument(--output string)
# format:
#        ((bool)success, True if the --output string had been successfully parsed
#         (bool)output to the console ?,
#         (bool)output to the logfile ?,
#         (str)logfile open mode = 'a' or 'w',
#         (str)logfile name,
#        )
OUTPUT = []

# progress bar length (in characters)
# 'None' is an accepted value and extends the length of the bar
# to the entire width of the terminal.
PROGRESSBAR_LENGTH = None

# units used in this project
UNITS = {'time': 'seconds',
         'string length': 'characters',
         'memory': 'bytes',
         }

# name of the log file
LOGFILE_NAME = "report.txt"

# name of the graphs file
GRAPHS_FILENAME = "report__SUFFIX__.png"
