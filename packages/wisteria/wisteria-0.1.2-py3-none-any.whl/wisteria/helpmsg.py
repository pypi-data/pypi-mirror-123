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
    Wisteria project : wisteria/helpmsg.py

    Some help messages

    ___________________________________________________________________________

    o  help_graphsfilenames()
"""
from wisteria.globs import GRAPHS_FILENAME
from wisteria.utils import normpath


def help_graphsfilenames():
    """
        help_graphsfilenames()

        Return a message describing where graphs files would be written
        on disk.

        _______________________________________________________________________

        RETURNED VALUE: (str)an help message
    """
    return f"'{GRAPHS_FILENAME.replace('__SUFFIX__', '1')}'" \
        f"({normpath(GRAPHS_FILENAME.replace('__SUFFIX__', '1'))}), " \
        f"'{GRAPHS_FILENAME.replace('__SUFFIX__', '2')}'" \
        f"({normpath(GRAPHS_FILENAME.replace('__SUFFIX__', '2'))}), " \
        "and so on"
