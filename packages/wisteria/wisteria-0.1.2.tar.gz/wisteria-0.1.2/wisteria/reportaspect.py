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
    Wisteria project : wisteria/reportaspect.py

    Define some 'aspects' (=some text attributes) for some excepts in report.

    ___________________________________________________________________________

    o  aspect_boolsuccess(bool_success)
    o  aspect_data(data_objectname)
    o  aspect_list(listitems)
    o  aspect_mem_usage(bytesnumber)
    o  aspect_nodata(string)
    o  aspect_nounplural(string, number)
    o  aspect_percentage(percentage)
    o  aspect_ratio(inttotal_and_floatratio)
    o  aspect_serializer0(serializer_name)
    o  aspect_serializer(serializer_name)
    o  aspect_stringlength(int_stringlength)
    o  aspect_time(floattime)
    o  aspect_title(title)

    o  aspect_exaequowith(item, listitems)
"""
import wisteria.globs


def aspect_boolsuccess(bool_success):
    """
        SerializationResults.aspect_boolsuccess()

        Format the input argument into a string. The input argument is a (bool)success.
            ex: False > "NOT OK"

        _______________________________________________________________

        ARGUMENT: (bool)bool_success

        RETURNED VALUE: a formatted string representing the (bool)bool_success.
    """
    if bool_success is None:
        return aspect_nodata()
    return "ok" if bool_success else "[red]NOT OK[/red]"


def aspect_data(data_objectname):
    """
        aspect_data()

        Modify the aspect of (str)data_objectname.

        _______________________________________________________________________

        ARGUMENT: (str)data_objectname

        RETURNED VALUE: (str)data_objectname + some text attributes.
    """
    return f"[bold white]{data_objectname}[/bold white]"


def aspect_list(listitems, func=None):
    """
        aspect_list()

        Return a (str)list of words written in good English, something
        like "a, b, and c" (no Oxford Comma here, confer
        https://www.grammar-monster.com/lessons/commas_the_Oxford_comma.htm)

        If <func> is not None, apply <func> to each item in <listitems>.

        _______________________________________________________________________

        ARGUMENTS:
        o  (list of str)listitems
        o  (callable)   func, the function to be applied to each item in
                        the result.

        RETURNED VALUE: (str)a formatted string with all items in <listitems>.
    """
    if len(listitems) == 0:
        return ""
    if len(listitems) == 1:
        return listitems[0] if not func else func(listitems[0])
    if len(listitems) == 2:
        return f"{func(listitems[0])} and {func(listitems[1])}"
    return f"{', '.join(func(listitem) for listitem in listitems[:-1])} and {func(listitems[-1])}"


def aspect_mem_usage(bytesnumber):
    """
        aspect_mem_usage()

        Modify the aspect of (int)bytesnumber.

        _______________________________________________________________________

        ARGUMENT: (int)bytesnumber

        RETURNED VALUE: (str)bytesnumber + some text attributes.
    """
    if bytesnumber is None:
        return aspect_nodata()
    if bytesnumber == 0:
        return "0 byte"
    if bytesnumber < 5000:
        return f"{bytesnumber} bytes"
    if bytesnumber < 95000:
        return f"{bytesnumber/1000:.1f} Ko"
    if bytesnumber < 95000000:
        return f"{bytesnumber/1000000:.1f} Mo"
    if bytesnumber < 95000000000:
        return f"{bytesnumber/1000000000:.1f} Go"
    return f"{bytesnumber/1000000000000:.1f} Po"


def aspect_nodata(string=None):
    """
        aspect_nodata()

        Return a string with rich text attribute saying that no data is available.

        _______________________________________________________________________

        ARGUMENT:(None or str)if string is None, a default string ("no data")
                 will be used; if string is a str, this string will be used.

        RETURNED VALUE: (str)"no data" string + some text attributes.
    """
    if not string:
        string = "(no data)"

    return f"[red]{string}[/red]"


def aspect_nounplural(string,
                      number):
    """
        aspect_nounplural()

        Return string with a final -s if <number> is greater than one.

        _______________________________________________________________________

        o  (str)string, a string ending with a word to which a final s may be added
        o  (int)number, 0 <= number

        RETURNED VALUE: (str)string + -s if <number> is greater than one.
    """
    if number <= 1:
        return string
    return string+"s"


def aspect_percentage(percentage):
    """
        aspect_percentage()

        Modify the aspect of (float)percentage.

        _______________________________________________________________________

        ARGUMENT: (float)percentage

        RETURNED VALUE: (str)percentage + some text attributes.
    """
    return f"{percentage:.2f}%"


def aspect_ratio(inttotal_and_floatratio):
    """
        SerializationResults.aspect_ratio()

        Format the input argument into a string. The input argument is an absolute
        (int)number and a (float)fraction, its ratio.
            ex: (3, 0.5) > "3 (50 %)"

        _______________________________________________________________

        ARGUMENT: (None|(int, float))inttotal_and_floatratio

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if inttotal_and_floatratio != (None, None):
        return f"{inttotal_and_floatratio[0]} " \
            f"({aspect_percentage(100*inttotal_and_floatratio[1])})"
    return aspect_nodata()


def aspect_serializer0(serializer_name):
    """
        aspect_serializer0()

        Modify the aspect of (str)serializer_name.

        _______________________________________________________________________

        ARGUMENT: (str)serializer_name

        RETURNED VALUE: (str)serializer_name + some text attributes.
    """
    return "[yellow]" \
        f"{serializer_name}" \
        "[/yellow]"


def aspect_serializer(serializer_name):
    """
        aspect_serializer()

        Modify the aspect of (str)serializer_name; if possible, replace it by its
        .human_name.

        _______________________________________________________________________

        ARGUMENT: (str)serializer_name

        RETURNED VALUE: (str)serializer_name + some text attributes.
    """
    if serializer_name in wisteria.globs.SERIALIZERS:
        return f"{aspect_serializer0(wisteria.globs.SERIALIZERS[serializer_name].human_name)}"
    return f"{aspect_serializer0(serializer_name)}"


def aspect_stringlength(int_stringlength):
    """
        SerializationResults.aspect_stringlength()

        Format the input argument into a string. The input argument is a (int)number
        of characters
            ex: 3 > "3 chars"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|int)int_stringlength, a string number.

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if int_stringlength is None:
        return aspect_nodata()
    return f"{int_stringlength}"


def aspect_time(floattime):
    """
        SerializationResults.aspect_time()

        Format the input argument into a string. The input argument is a (float)time laps.
            ex: 0.333345677 > "0.333345"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|float)floattime

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if floattime is None:
        return aspect_nodata()
    return f"{floattime:.6f}"


def aspect_title(title):
    """
        aspect_title()

        Modify the aspect of (str)title.

        _______________________________________________________________________

        ARGUMENT: (str)title

        RETURNED VALUE: (str)title + some text attributes.
    """
    return f"[bold white on blue]{title}[/bold white on blue]"


# function defined here since it depends from aspect_list().
def aspect_exaequowith(item,
                       listitems,
                       func=aspect_serializer,
                       prefix=", [i]ex aequo[/i] with "):
    """
        aspect_exaequowith()

        <listitems> is a list of (str)items, <item> being one of the items,
        something like: listitems=['a', 'b', 'c'], items="b".
        This function will return <prefix>(~"ex aequo") + "a and c".

        _______________________________________________________________________

        ARGUMENTS:
        o  (str)           item
        o  (list of str)   listitems
        o  (callable)      func        , callable that will be called upon each <item>.
        o  (str)           prefix      , string that will be added before the result

        RETURNED VALUE: (str)
    """
    if len(listitems) == 1:
        return ""
    listitems.remove(item)
    return prefix + aspect_list(listitems, func)
