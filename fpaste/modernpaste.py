"""
Modernpaste handler for fpaste

File: modernpaste.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import json
import time
import urllib
from fpaste.utils import is_text, confirm, USER_AGENT
import logging
import textwrap
from logger import get_module_logger


# Logger for these functions
lgr = get_module_logger("stikked", logging.INFO)


def paste(text, options):
    """Send text to paste server and return the URL."""
    if not text:
        lgr.warn("No text to send.")
        return False

    # if sent data exceeds maxlength, server dies without error returned, so,
    # we'll truncate the input here, until the server decides to truncate
    # instead of die
    data = json.dumps(
        {'language': options.lang, 'contents': text,
         'title': options.title,
         'expiry_time': int(options.expires) + int(time.time()),
         'password': options.password}).encode('utf8')
    pasteSizeKiB = len(data)/1024.0

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
        url=options.url + '/submit',
        data=data,
        headers={
            'User-agent': USER_AGENT,
            'Content-Type': 'application/json'})
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
        "apl",
        "asn.1",
        "asterisk",
        "brainfuck",
        "clike",
        "clojure",
        "gss",
        "cmake",
        "cobol",
        "coffeescript",
        "commonlisp",
        "crystal",
        "css",
        "cypher",
        "python",
        "d",
        "dart",
        "django",
        "dockerfile",
        "diff",
        "dtd",
        "dylan",
        "ebnf",
        "ecl",
        "eiffel",
        "elm",
        "erlang",
        "factor",
        "fcl",
        "forth",
        "fortran",
        "mllike",
        "gas",
        "gherkin",
        "go",
        "groovy",
        "haml",
        "handlebars",
        "haskell",
        "haxe",
        "html",
        "htmlembedded",
        "htmlmixed",
        "http",
        "idl",
        "clike",
        "jade",
        "javascript",
        "jinja2",
        "julia",
        "kotlin",
        "less",
        "livescript",
        "lua",
        "markdown",
        "mathematica",
        "mbox",
        "mirc",
        "modelica",
        "mscgen",
        "mumps",
        "nginx",
        "nsis",
        "ntriples",
        "clike",
        "mllike",
        "octave",
        "oz",
        "pascal",
        "pegjs",
        "perl",
        "asciiarmor",
        "php",
        "pig",
        "powershell",
        "properties",
        "protobuf",
        "puppet",
        "python",
        "q",
        "r",
        "rpm",
        "rst",
        "ruby",
        "rust",
        "sas",
        "sass",
        "spreadsheet",
        "scala",
        "scheme",
        "scss",
        "shell",
        "sieve",
        "slim",
        "smalltalk",
        "smarty",
        "solr",
        "soy",
        "stylus",
        "sql",
        "sparql",
        "swift",
        "stex",
        "tcl",
        "textile",
        "tiddlywiki",
        "tiki",
        "toml",
        "tornado",
        "troff",
        "ttcn",
        "ttcn-cfg",
        "turtle",
        "twig",
        "text",
        "vb",
        "vbscript",
        "velocity",
        "verilog",
        "vhdl",
        "vue",
        "webidl",
        "xml",
        "xquery",
        "yacas",
        "yaml",
        "yaml-frontmatter",
        "Full list at: https://codemirror.net/mode/"
    ],
    "validExpiresOpts": ['1800', '21600', '86400', '604800', '2592000'],
    "ext2lang_map": {
        'sh': 'shell',
        'bash': 'shell',
        'c': 'clike',
        'h': 'clike',
        'hpp': 'clike',
        'cpp': 'clike',
        'css': 'css',
        'diff': 'diff',
        'html': 'html',
        'htm': 'html',
        'ini': 'ini',
        'java': 'java',
        'js': 'javascript',
        'jsp': 'htmlembedded',
        'lua': 'lua',
        'mbox': 'mbox',
        'md': 'markdown',
        'pl': 'perl',
        'php': 'php',
        'php3': 'php',
        'py': 'python',
        'r': 'r',
        'rb': 'ruby',
        'rhtml': 'html',
        'rst': 'rst',
        'sql': 'sql',
        'sqlite': 'sql',
        'sty': 'stex',
        'tcl': 'tcl',
        'tex': 'stex',
        'xml': 'xml'}
}
