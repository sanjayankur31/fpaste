#!/usr/bin/env python3
"""
stikked handler for fpaste.

File: stikked.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import logging
from logger import get_module_logger
import textwrap
from fpaste.utils import is_text, confirm, USER_AGENT
import urllib
import json


APIKEY = "5uZ30dTZE1a5V0WYhNwcMddBRDpk6UzuzMu-APKM38iMHacxdA0n4vCqA34avNyt"

# Logger for these functions
lgr = get_module_logger("stikked", logging.INFO)


def paste(text, options):
    """Send text to paste server and return the URL."""
    if not text:
        lgr.warn("No text to send.")
        return False

    pasteSizeKiB = len(text)/1024.0

    # 512KiB appears to be the current hard limit (20110404); old limit was
    # 16MiB
    if pasteSizeKiB >= 512:
        lgr.warn(
            textwrap.dedent("""\
            Your paste size ({:.1}KiB) is very large and may be rejected by the
            server. A pastebin is NOT a file hosting
            service!""").format(pasteSizeKiB))
    # verify that it's most likely *non-binary* data being sent.
    if not is_text(text):
        lgr.warn(
            "Your paste looks a lot like binary data instead of text."
        )
        if not confirm("Send binary data anyway?"):
            return False

    req = urllib.request.Request(
        url=options['url'] + '?apikey={}'.format(APIKEY),
        data=text,
        headers={
            'User-agent': USER_AGENT
        })
    if options.proxy:
        if options.debug:
            lgr.info("Using proxy: {}".format(options.proxy))
        req.set_proxy(options.proxy, 'http')

    lgr.info("Uploading ({:.1}KiB)...".format(pasteSizeKiB))
    try:
        f = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            lgr.error("Error Uploading: {}".format(e.reason))
        elif hasattr(e, 'code'):
            lgr.error("Server Error: {} - {}".format(e.code, e.msg))
            if options.debug:
                lgr.debug(f.read())
        return False

    try:
        response = json.loads(f.read().decode("utf-8", "replace"))
    except ValueError as e:
        lgr.error(
            "Server did not return a correct JSON response: {}".format(e)
        )
        return False

    url = response['url']
    return url


options = {
    "validSyntaxOpts": [
        "text",
        "html5",
        "css",
        "javascript",
        "php",
        "python",
        "ruby",
        "lua",
        "bash",
        "erlang",
        "go",
        "c",
        "cpp",
        "diff",
        "latex",
        "sql",
        "xml",
        "0",
        "4cs",
        "6502acme",
        "6502kickass",
        "6502tasm",
        "68000devpac",
        "abap",
        "actionscript",
        "actionscript3",
        "ada",
        "aimms",
        "algol68",
        "apache",
        "applescript",
        "apt_sources",
        "arm",
        "asm",
        "asymptote",
        "asp",
        "autoconf",
        "autohotkey",
        "autoit",
        "avisynth",
        "awk",
        "bascomavr",
        "basic4gl",
        "bbcode",
        "bf",
        "bibtex",
        "blitzbasic",
        "bnf",
        "boo",
        "c_loadrunner",
        "c_mac",
        "c_winapi",
        "caddcl",
        "cadlisp",
        "cfdg",
        "cfm",
        "chaiscript",
        "chapel",
        "cil",
        "clojure",
        "cmake",
        "cobol",
        "coffeescript",
        "cpp-winapi",
        "csharp",
        "cuesheet",
        "d",
        "dart",
        "dcs",
        "dcl",
        "dcpu16",
        "delphi",
        "div",
        "dos",
        "dot",
        "e",
        "ecmascript",
        "eiffel",
        "email",
        "epc",
        "euphoria",
        "ezt",
        "f1",
        "falcon",
        "fo",
        "fortran",
        "freebasic",
        "freeswitch",
        "fsharp",
        "gambas",
        "gdb",
        "genero",
        "genie",
        "gettext",
        "glsl",
        "gml",
        "gnuplot",
        "groovy",
        "gwbasic",
        "haskell",
        "haxe",
        "hicest",
        "hq9plus",
        "html4strict",
        "icon",
        "idl",
        "ini",
        "inno",
        "intercal",
        "io",
        "ispfpanel",
        "j",
        "java",
        "java5",
        "jcl",
        "jquery",
        "klonec",
        "klonecpp",
        "kotlin",
        "lb",
        "ldif",
        "lisp",
        "llvm",
        "locobasic",
        "logcat",
        "logtalk",
        "lolcode",
        "lotusformulas",
        "lotusscript",
        "lscript",
        "lsl2",
        "m68k",
        "magiksf",
        "make",
        "mapbasic",
        "matlab",
        "mirc",
        "mmix",
        "modula2",
        "modula3",
        "mpasm",
        "mxml",
        "mysql",
        "nagios",
        "netrexx",
        "newlisp",
        "nginx",
        "nimrod",
        "nsis",
        "oberon2",
        "objc",
        "objeck",
        "ocaml",
        "octave",
        "oobas",
        "oorexx",
        "oracle11",
        "oracle8",
        "oxygene",
        "oz",
        "parasail",
        "parigp",
        "pascal",
        "pcre",
        "per",
        "perl",
        "perl6",
        "pf",
        "pic16",
        "pike",
        "pixelbender",
        "pli",
        "plsql",
        "postgresql",
        "postscript",
        "povray",
        "powerbuilder",
        "powershell",
        "proftpd",
        "progress",
        "prolog",
        "properties",
        "providex",
        "purebasic",
        "pys60",
        "q",
        "qbasic",
        "qml",
        "racket",
        "rails",
        "rbs",
        "rebol",
        "reg",
        "rexx",
        "robots",
        "rpmspec",
        "rsplus",
        "rust",
        "sas",
        "scala",
        "scheme",
        "scilab",
        "scl",
        "sdlbasic",
        "smalltalk",
        "smarty",
        "spark",
        "sparql",
        "standardml",
        "stonescript",
        "systemverilog",
        "tcl",
        "teraterm",
        "thinbasic",
        "tsql",
        "typoscript",
        "unicon",
        "uscript",
        "upc",
        "urbi",
        "vala",
        "vb",
        "vbnet",
        "vbscript",
        "vedit",
        "verilog",
        "vhdl",
        "vim",
        "visualfoxpro",
        "visualprolog",
        "whitespace",
        "whois",
        "winbatch",
        "xbasic",
        "xorg_conf",
        "xpp",
        "yaml",
        "z80",
        "zxbasic"
    ],
    "validExpiresOpts": ['1800', '21600', '86400'],
    "ext2lang_map": {
        'sh': 'bash',
        'bash': 'bash',
        'bib': 'bibtex',
        'c': 'c',
        'cpp': 'cpp',
        'css': 'css',
        'diff': 'diff',
        'h': 'c',
        'hpp': 'cpp',
        'html': 'html',
        'htm': 'html',
        'ini': 'ini',
        'java': 'java',
        'js': 'javascript',
        'lua': 'lua',
        'pl': 'perl',
        'php': 'php',
        'php3': 'php',
        'py': 'python',
        'rb': 'ruby',
        'rhtml': 'html',
        'sql': 'sql',
        'sqlite': 'sql',
        'sty': 'latex',
        'tcl': 'tcl',
        'tex': 'latex',
        'xml': 'xml'}
}
