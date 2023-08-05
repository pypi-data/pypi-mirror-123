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
    Wisteria project : wisteria/cmdline_cmp.py

    Just the parsing of the --cmp argument.

    ___________________________________________________________________________

    o  read_cmpstring(cmpstring)
"""
import re

from wisteria.msg import msgerror
from wisteria.globs import REGEX_CMP, REGEX_CMP__HELP
from wisteria.reportaspect import aspect_serializer0, aspect_serializer, aspect_nounplural
import wisteria.globs


def read_cmpstring(cmpstring):
    """
        read_cmpstring()

        Return a simpler representation of (str)<cmpstring>.

        Some valid examples, "..." being "(bool/success)True".
        --cmp="jsonpickle vs all (all)"
        --cmp="jsonpickle vs all"
        --cmp="jsonpickle"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (cmpdata/str)"all"

        --cmp="jsonpickle (ini)"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (cmpdata/str)"ini"

        --cmp="jsonpickle vs json"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"json", (cmpdata/str)"all"

        "vs" may be used as well as "versus" or "against".

        _______________________________________________________________________

        ARGUMENT: (str)cmpstring, the source string to be read.
                syntax: "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

        RETURNED VALUE: (bool)success,
                        (str)serializer1,
                        (str)serializer2,
                        (str:"all|cwc|ini")cmpdata
    """
    serializers = wisteria.globs.SERIALIZERS
    u_serializers = wisteria.globs.UNAVAILABLE_SERIALIZERS

    if res := re.match(REGEX_CMP, cmpstring):
        serializer1 = res.group("serializer1")
        if serializer1 is None or serializer1 == "others":
            serializer1 = "all"
        serializer2 = res.group("serializer2")
        if serializer2 is None or serializer2 == "others":
            serializer2 = "all"
        cmpdata = res.group("cmpdata")
        if cmpdata is None:
            cmpdata = "all"

        # error: serializer1 is not in SERIALIZERS among UNAVAILABLE_SERIALIZES.
        if serializer1 in u_serializers:
            # BEWARE !
            # DO NOT USE aspect_serializer() instead of aspect_serializer0()
            # to display acceptable serializers name
            # since 'Iaswn' isn't an acceptable name, but 'iaswn' is.
            msgerror(
                f"(ERRORID045) {aspect_serializer0(serializer1)} is a known serializer "
                f"but the corresponding package has not been installed. "
                "Try $ wisteria --checkup for more informations.")
            return False, None, None, None

        # error: serializer1 is an unknown serializer.
        if not (serializer1 == "all" or serializer1 in serializers):
            # BEWARE !
            # DO NOT USE aspect_serializer() instead of aspect_serializer0()
            # to display acceptable serializers name
            # since 'Iaswn' isn't an acceptable name, but 'iaswn' is.
            msgerror(
                "(ERRORID009) Unknown serializer (for --cmp position 1) "
                f"read in the --cmp string '{cmpstring}': "
                f"what is '{serializer1}' ? "
                "Known serializers for position 1 are "
                f"{aspect_serializer('all')} and "
                f"{', '.join(aspect_serializer0(serial) for serial in serializers)} . "
                "Unavailable "
                f"{aspect_nounplural('serializer', len(u_serializers))} "
                ": "
                f"{', '.join(aspect_serializer(serial) for serial in u_serializers)} . "
                "Try $ wisteria --checkup for more informations.")
            return False, None, None, None

        # error: serializer2 is not in SERIALIZERS among UNAVAILABLE_SERIALIZES.
        if serializer2 in u_serializers:
            # BEWARE !
            # DO NOT USE aspect_serializer() instead of aspect_serializer0()
            # to display acceptable serializers name
            # since 'Iaswn' isn't an acceptable name, but 'iaswn' is.
            msgerror(
                f"(ERRORID046) {aspect_serializer0(serializer2)} is a known serializer "
                f"but the corresponding package has not been installed. "
                "Try $ wisteria --checkup for more informations.")
            return False, None, None, None

        # error: serializer2 is an unknown serializer.
        if not (serializer2 == "all" or serializer2 == "others" or serializer2 in serializers):
            # BEWARE !
            # DO NOT USE aspect_serializer() instead of aspect_serializer0()
            # to display acceptable serializers name
            # since 'Iaswn' isn't an acceptable name, but 'iaswn' is.
            msgerror(
                "(ERRORID010) Unknown serializer (for --cmp position 2) "
                f"read in the --cmp string '{cmpstring}': "
                f"what is '{serializer2}' ? "
                f"Known serializers for position 2 are "
                f"{aspect_serializer('all')}, {aspect_serializer('others')} and "
                f"{', '.join(aspect_serializer0(serial) for serial in serializers)} . "
                "Unavailable "
                f"{aspect_nounplural('serializer', len(u_serializers))} "
                ": "
                f"{', '.join(aspect_serializer(serial) for serial in u_serializers)} . "
                "Try $ wisteria --checkup for more informations.")
            return False, None, None, None
        if serializer1 == serializer2 and serializer1 != "all":
            msgerror(
                f"(ERRORID011) Both serializer-s from cmp string '{cmpstring}' "
                f"(here, both set to '{serializer1}') "
                "can't have the same value, 'all' and 'all' excepted.")
            return False, None, None, None

        return True, serializer1, serializer2, cmpdata

    msgerror(f"(ERRORID012) Ill-formed cmp string '{cmpstring}'. "
             f"Expected syntax is '{REGEX_CMP__HELP}'.")
    return False, None, None, None
