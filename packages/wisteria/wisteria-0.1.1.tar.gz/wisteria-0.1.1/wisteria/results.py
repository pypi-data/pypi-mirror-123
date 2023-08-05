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
    Wisteria project : wisteria/results.py

    Fonctions to compute results, especially compute_results().

    ___________________________________________________________________________

    o  get_serializers_selection(serializer1, serializer2)
    o  get_data_selection(cmpdata, config)
    o  compute_results(config, serializer1, serializer2, cmpdata)
"""
from rich.console import Console
from rich.progress_bar import ProgressBar

import wisteria.data
import wisteria.globs
from wisteria.globs import VERBOSITY_MINIMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.globs import PROGRESSBAR_LENGTH
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msgdebug, msginfo, msgerror
from wisteria.serializers_classes import SerializationResults
from wisteria.utils import strdigest
from wisteria.reportaspect import aspect_serializer


def get_serializers_selection(serializer1,
                              serializer2):
    """
        get_serializers_selection()

        Return a tuple of all serializers defined by (str)<serializer1>, (str)<serializer2>.

        _______________________________________________________________________

        ARGUMENTS:
        o    <serializer1> : value returned by read_cmpstring()
        o    <serializer2> : value returned by read_cmpstring()

        RETURNED VALUE: a tuple of str, i.e. all serializers defined by (str)<serializer1>,
                        (str)<serializer2>
    """
    res = set()

    if serializer1 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer1)

    if serializer2 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer2)

    return tuple(res)


def get_data_selection(cmpdata,
                       config):
    """
        get_data_selection()

        Return a tuple of the data objects names selected by the <config>.

        _______________________________________________________________________

        ARGUMENTS:
        o  cmpdata: (str)"all" or "ini"
        o  config:  (dict) dict returned by read_cfgfile()

        RETURNED VALUE: (tuple) a tuple of (str)data keys
    """
    res = []

    if cmpdata == "all":
        res = tuple(wisteria.globs.DATA.keys())
    elif cmpdata == "ini":
        if config["data selection"]["data selection"] == "all":
            res = tuple(config["objects"].keys())
        elif config["data selection"]["data selection"] == "only if yes":
            res = (data_name for data_name in config["data objects"]
                   if config["data objects"][data_name])
        elif config["data selection"]["data selection"].startswith("data set/"):
            res = tuple(config["data sets"][config["data selection"]["data selection"]])
        else:
            raise WisteriaError(
                "(ERRORID020) "
                "Can't understand a value given to \\[data selection]'data selection': "
                f"what is '{config['data selection']['data selection']}' ? "
                "Known values are 'all', 'ini' and 'data set/xxx' "
                "where xxx is a string.")
    else:
        raise WisteriaError(
            "(ERRORID021) Can't understand a value given to the 'data' part in --cmp: "
            f"what is '{cmpdata}' ? "
            "Known values are 'all' and 'ini'. ")

    return res


def compute_results(config,
                    serializer1,
                    serializer2,
                    cmpdata):
    """
        compute_results()

        Create a SerializationResults object and try to fill it with all
        required encodings/decodings defined by <serializer1>,
        <serializer2> and <cmpdata>.

        _______________________________________________________________________

        ARGUMENTS:
        o  config               : None if no config file, otherwise the dict
                                  returned by read_cfgfile().
        o  (str)serializer1
        o  (str)serializer2
        o  (str)cmpdata         : 'all', 'ini' or 'cwc'

        RETURNED VALUE:    (SerializationResults, None) if no error occured
                        or (None, (int)exit_code) if an error occured
    """
    def erase_progress_bar():
        """
            erase_progress_bar()

            Erase the progress bar so that it is possible to write text over
            the ancient progress bar.

            Show the cursor.
        """
        if wisteria.globs.ARGS.verbosity not in (VERBOSITY_MINIMAL, VERBOSITY_DEBUG):
            # the following lines make the progress bar disappear.
            # the next rprint() will overwrite the spaces that are about
            # to be added:
            if PROGRESSBAR_LENGTH is None:
                console.file.write(" "*console.width)
            else:
                console.file.write(" "*PROGRESSBAR_LENGTH)
            console.file.write("\r")

            console.show_cursor(True)

    try:
        # serializers and data to be used through the tests:
        _serializers = get_serializers_selection(serializer1, serializer2)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"serializers to be used are: {_serializers}")
        _dataobjs = get_data_selection(cmpdata, config)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"data objs to be used are: {_dataobjs}")

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo("Please wait until all required encodings/decodings have been computed.")

        results = SerializationResults()

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        # Please note that there can be NO progress bar if verbosity is set to minimal:
        # it's important for scripts calling this project from the outside.
        if wisteria.globs.ARGS.verbosity not in (VERBOSITY_MINIMAL, VERBOSITY_DEBUG):
            console = Console()
            progressbar = ProgressBar(width=PROGRESSBAR_LENGTH,
                                      total=len(_serializers)*len(_dataobjs))
            console.show_cursor(False)
            progressbar_index = 0

        for serializer in sorted(_serializers):
            results[serializer] = {}
            for data_name in sorted(_dataobjs):
                fingerprint = strdigest(serializer+data_name)

                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"About to call function for serializer='{serializer}' "
                             f"and data name='{data_name}' "
                             f"[{fingerprint}]")

                results[serializer][data_name] = wisteria.globs.SERIALIZERS[serializer].func(
                    action="serialize",
                    obj=wisteria.globs.DATA[data_name],
                    fingerprint=fingerprint)

                # (progress bar)
                # Please note that there can be NO progress bar if the debug mode is enabled:
                # the output can't display both correctly.
                # Please note that there can be NO progress bar if verbosity is set to minimal:
                # it's important for scripts calling this project from the outside.
                if wisteria.globs.ARGS.verbosity not in (VERBOSITY_MINIMAL, VERBOSITY_DEBUG):
                    progressbar_index += 1
                    progressbar.update(progressbar_index)
                    console.print(progressbar)
                    console.file.write("\r")

                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"result: {results[serializer][data_name]} "
                             f"[{fingerprint}]")

            # we can't yet use results.total_encoding_strlen() since .finish_initialization()
            # has not be called:
            if sum(results[serializer][dataobj].encoding_strlen
                   for dataobj in results[serializer]
                   if results[serializer][dataobj] is not None and
                   results[serializer][dataobj].encoding_strlen is not None) == 0 and \
               not wisteria.globs.ARGS.tolerateabsurdvalues:
                erase_progress_bar()
                msgerror("(ERRORID043) Absurd value computed "
                         f"for serializer {aspect_serializer(serializer)} : "
                         "Σ sum(results[serializer][dataobj].encoding_strlen) is 0.")
                # (pimydoc)exit codes
                # ⋅*  0: normal exit code
                # ⋅*  1: normal exit code after --checkup
                # ⋅*  2: normal exit code after --downloadconfigfile
                # ⋅*  3: normal exit code after --mymachine
                # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
                # ⋅* -2: error, ill-formed --cmp string
                # ⋅* -3: internal error, data can't be loaded
                # ⋅* -4: internal error, an error occured while computing the results
                # ⋅* -5: internal error, an error in main()
                # ⋅* -6: error, ill-formed --output string
                # ⋅* -7: error, an absurd value has been computed
                return None, -7

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        # Please note that there can be NO progress bar if verbosity is set to minimal:
        # it's important for scripts calling this project from the outside.
        erase_progress_bar()

        if not results.finish_initialization():
            msgerror("(ERRORID015) Incorrect data, the program has to stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅*  3: normal exit code after --mymachine
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            # ⋅* -4: internal error, an error occured while computing the results
            # ⋅* -5: internal error, an error in main()
            # ⋅* -6: error, ill-formed --output string
            # ⋅* -7: error, an absurd value has been computed
            return None, -3
        if results.dataobjs_number == 0:
            msginfo("No data to handle, the program can stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅*  3: normal exit code after --mymachine
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            # ⋅* -4: internal error, an error occured while computing the results
            # ⋅* -5: internal error, an error in main()
            # ⋅* -6: error, ill-formed --output string
            # ⋅* -7: error, an absurd value has been computed
            return None, 2

        return results, None

    except WisteriaError as exception:
        msgerror(f"An error occured: {exception}")

        # (pimydoc)exit codes
        # ⋅*  0: normal exit code
        # ⋅*  1: normal exit code after --checkup
        # ⋅*  2: normal exit code after --downloadconfigfile
        # ⋅*  3: normal exit code after --mymachine
        # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
        # ⋅* -2: error, ill-formed --cmp string
        # ⋅* -3: internal error, data can't be loaded
        # ⋅* -4: internal error, an error occured while computing the results
        # ⋅* -5: internal error, an error in main()
        # ⋅* -6: error, ill-formed --output string
        # ⋅* -7: error, an absurd value has been computed
        return None, -4
