#!/usr/bin/env python3
"""
Helper functions to gather system information for fpaste

File: sysinfo.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import sys
import subprocess



def get_sysinfo(cmdlist):
    """
    Main worker function that runs various commands to gather system
    information.

    :cmdlist: List of diagnostic commands.
    :returns: String with gathered information.

    """
    pass


def sysinfo(
        show_stderr=False, show_successful_cmds=True, show_failed_cmds=True):
    """Return commonly requested system info."""
    # 'ps' output below has been anonymized: -n for uid vs username, and -c for
    # short processname
    si = []
    print("Gathering system info", end=' ', file=sys.stderr)
    for cmds in cmdlist:
        cmdname = cmds[0]
        cmd = ""
        for cmd in cmds[1:]:
            sys.stderr.write('.')  # simple progress feedback
            p = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            try:
                (out, err) = p.communicate(timeout=300)
            except subprocess.TimeoutExpired:
                p.kill()
                (out, err) = p.communicate()
            if not p.returncode == 0:
                if show_stderr:
                    if err:
                        print(
                            "sysinfo Error: the cmd \"%s\" returned %d with stderr: %s" %
                            (cmd, p.returncode, err), file=sys.stderr)
                    else:
                        print(
                            "sysinfo Error: the cmd \"%s\" returned %d without errors" %
                            (cmd, p.returncode), file=sys.stderr)
                    print("Trying next fallback cmd...", file=sys.stderr)
            if p.returncode == 0 and out:
                break
        if out:
            if show_successful_cmds:
                si.append(('%s (%s)' % (cmdname, cmd), out))
            else:
                si.append(('%s' % cmdname, out))
        else:
            if show_failed_cmds:
                si.append(
                    ('%s (without results: "%s")' %
                     (cmdname,
                      '" AND "'.join(
                          cmds[
                              1:])),
                        out))
            else:
                si.append(('%s' % cmdname, out))

    # return in readable indented format
    sistr = "=== fpaste %s System Information (fpaste --sysinfo) ===\n" % VERSION
    for cmdname, output in si:
        sistr += "* %s:\n" % cmdname
        if not output:
            sistr += "     N/A\n\n"
        else:
            for line in output.decode("utf-8", "replace").split('\n'):
                sistr += "     %s\n" % line

    return sistr
