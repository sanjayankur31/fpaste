#!/usr/bin/env python3
"""fpaste - a cli frontend for the fpaste.org pastebin."""

# Copyright 2008, 2010 Fedora Unity Project (http://fedoraunity.org)
# Author: Jason 'zcat' Farrell <farrellj@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import textwrap
import toml
from toml import TomlDecodeError
import logging
from logger import get_module_logger

# Logger for these functions
lgr = get_module_logger("utils", logging.INFO)


def is_text(text, maxCheck=100, pctPrintable=0.75):
    """
    Check to see if a majority of the characters are printable.

    Returns true if maxCheck evenly distributed chars in text are >=
    pctPrintable% text chars.
    """
    # e.g.: /bin/* ranges between 19% and 42% printable
    from string import printable
    if type(text) == bytes:
        text = text.decode("utf-8", "replace")
    nchars = len(text)
    if nchars == 0:
        return False
    ncheck = min(nchars, maxCheck)
    inc = float(nchars)/ncheck
    i = 0.0
    nprintable = 0
    while i < nchars:
        if text[int(i)] in printable:
            nprintable += 1
        i += inc
    pct = float(nprintable) / ncheck
    return (pct >= pctPrintable)


def confirm(prompt="OK?"):
    """Prompt user for yes/no input and return True or False."""
    prompt += " [y/N]: "
    try:
        ans = input(prompt)
    except EOFError:    # already read sys.stdin and hit EOF
        # rebind sys.stdin to user tty (unix-only)
        try:
            mytty = os.ttyname(sys.stdout.fileno())
            sys.stdin = open(mytty)
            ans = input()
        except:
            lgr.error(textwrap.dedent("""
                could not rebind sys.stdin to {} after sys.stdin EOF
                """).format(mytty))
            return False

    if ans.lower().startswith("y"):
        return True
    else:
        return False


def summarize_text(text):
    # use beginning/middle/end content snippets as a description summary. 120
    # char limit
    # "36chars ... 36chars ... 36chars" == 118 chars
    # TODO: nuking whitespace in huge text files might be expensive; optimize
    # for b/m/e segments only
    sniplen = 36
    seplen = len(" ... ")
    tsum = ""
    text = " ".join(text.split())   # nuke whitespace
    tlen = len(text)

    if tlen < sniplen+seplen:
        tsum += text
    if tlen >= sniplen+seplen:
        tsum += text[0:sniplen] + " ..."
    if tlen >= (sniplen*2)+seplen:
        tsum += " " + text[tlen/2-(sniplen/2):(tlen/2)+(sniplen/2)] + " ..."
    if tlen >= (sniplen*3)+(seplen*2):
        tsum += " " + text[-sniplen:]
    # print >> sys.stderr, str(len(tsum)) + ": " + tsum

    return tsum


def read_config(config_file=None):
    """Load the config file.

    :config_file: path to config file.
    :returns: TODO

    """
    config = {}
    fpaste_config_file = None
    # If the user specified config file exists, use that
    if config_file:
        if os.path.isfile(config_file):
            fpaste_config_file = config_file
    else:
        # Try the default locations in order
        # First the user config dir
        system_config_file = os.path.join('/etc', "fpaste",
                                          "fedora-config.toml")

        xdg_config_dir = None
        # Not always defined. WTH
        if 'XDG_CONFIG_DIR' in os.environ:
            xdg_config_dir = os.environ['XDG_CONFIG_DIR']
        else:
            # This environment variable must be defined
            home_dir = os.environ['HOME']
            xdg_config_dir = os.path.join(home_dir, '.config')

        user_config = os.path.join(
            xdg_config_dir, "fpaste", "fedora-config.toml"
        )

        if os.path.isfile(user_config):
            fpaste_config_file = user_config
        elif os.path.isfile(system_config_file):
            fpaste_config_file = system_config_file
        else:
            lgr.error("No config file found. Exiting.")
            return False

    # Read what we have
    lgr.debug("Using {}".format(fpaste_config_file))
    try:
        config = toml.load(fpaste_config_file)
    except TomlDecodeError as e:
        lgr.error("Unable to load file {}: ".format(
            fpaste_config_file, e))
        return False
    return config