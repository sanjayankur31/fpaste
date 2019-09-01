#!/usr/bin/env python3
"""
Helper functions to gather system information for fpaste

File: sysinfo.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import subprocess
import textwrap
from version import __version__
import logging
from logger import get_module_logger

# Logger for these functions
logger = get_module_logger("sysinfo", logging.INFO)


def get_sysinfo(cmds):
    """
    Main worker function that runs various commands to gather system
    information.

    :cmds: List of diagnostic commands.
    :returns: String with gathered information.

    """
    logger.info("Gathering system info")
    output_string = textwrap.dedent("""\
    === fpaste {} System Information (fpaste --sysinfo) ===\n
    """).format(__version__)

    for cmd, cmd_list in cmds.items():
        output_list = run_cmd(cmd_list)
        output_string += "* {}:\n".format(cmd)

        if output_list['status'] == "OK":
            for output in output_list['commands']:
                if output['status'] == "OK":
                    info = output['output']
                    for line in info.decode("utf-8", "replace").split('\n'):
                        output_string += "     {}\n".format(line)
        else:
            output_string += "     N/A\n\n"

    return output_string


def run_cmd(cmd_list, show_progress=True):
    """
    Run command, return output.

    If a list of commands is provided, it runs them in order, only moving to
    the next in the list if the current one fails.

    :cmd_list: command to run.
    :show_progress: Boolean, show progress
    :returns: output from the command

    """
    # Store output status
    output_list = {}
    # Assume at least ne command succeeded
    output_list['status'] = "OK"
    # Output from each command if there are multiple
    output_list['commands'] = []
    for cmd in cmd_list:
        output = {}
        if show_progress:
            logger.info('Running {}'.format(cmd))
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        try:
            (out, err) = p.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            p.kill()
            (out, err) = p.communicate()
        if not p.returncode == 0:
            output_list['status'] = "Failed"
            output['status'] = "Failed"
            if err:
                output['error'] = err
                logger.warn(
                    "Command \"{}\" returned {} with stderr: {}".format(
                        cmd, p.returncode, err
                    )
                )
            else:
                logger.warn(
                    "Command \"{}\" returned {} without errors".format(
                        cmd, p.returncode
                    )
                )
        if p.returncode == 0 and out:
            output_list['status'] = "OK"
            output['status'] = "OK"
            output['output'] = out
            logger.debug("{}:\n{}".format(cmd, out))
        else:
            output_list['status'] = "OK"
            output['status'] = "OK"
            output['output'] = b"NA"
            logger.debug("{}:\n{}".format(cmd, out))

        output_list['commands'].append(output)
    # Return the gathered outputs
    return output_list
