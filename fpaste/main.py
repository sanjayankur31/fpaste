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
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import subprocess
import time
import json
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP


VERSION = '0.3.9.2'
USER_AGENT = 'fpaste/' + VERSION
FPASTE_URL = 'https://paste.fedoraproject.org/api/paste'


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
            print(
                "could not rebind sys.stdin to %s after sys.stdin EOF" %
                mytty,
                file=sys.stderr)
            return False

    if ans.lower().startswith("y"):
        return True
    else:
        return False


def paste(text, options):
    """Send text to paste server and return the URL."""
    if not text:
        print("No text to send.", file=sys.stderr)
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
        print(
            "WARNING: your paste size (%.1fKiB) is very large and may be rejected by the server. A pastebin is NOT a file hosting service!" %
            (pasteSizeKiB),
            file=sys.stderr)
    # verify that it's most likely *non-binary* data being sent.
    if not is_text(text):
        print(
            "WARNING: your paste looks a lot like binary data instead of text.",
            file=sys.stderr)
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
            print("Using proxy: %s" % options.proxy, file=sys.stderr)
        req.set_proxy(options.proxy, 'http')

    print("Uploading (%.1fKiB)..." % pasteSizeKiB, file=sys.stderr)
    try:
        f = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print("Error Uploading: %s" % e.reason, file=sys.stderr)
        elif hasattr(e, 'code'):
            print("Server Error: %d - %s" % (e.code, e.msg), file=sys.stderr)
            if options.debug:
                print(f.read())
        return False

    try:
        response = json.loads(f.read().decode("utf-8", "replace"))
    except ValueError as e:
        print(
            "Error: Server did not return a correct JSON response",
            file=sys.stderr)
        return False

    url = response['url']
    return url


def summarize_text(text):
    # use beginning/middle/end content snippets as a description summary. 120 char limit
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


def main():
    """Main work function."""
    validExpiresOpts = ['1800', '21600', '86400', '604800', '2592000']
    validSyntaxOpts = [
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
    ]
    validClipboardSelectionOpts = ['primary', 'secondary', 'clipboard']
    ext2lang_map = {
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

    usage = """\
Usage: %%prog [OPTION]... [FILE]...
  send text file(s), stdin, or clipboard to the %s pastebin and return the URL.

Examples:
  %%prog file1.txt file2.txt
  dmesg | %%prog
  (prog1; prog2; prog3) | fpaste
  %%prog --sysinfo -d "my pass" --confirm
  %%prog -t "debug output" -d "my pass" -l python foo.py""" % FPASTE_URL

    parser = OptionParser(usage=usage, version='%prog '+VERSION)
    parser.add_option(
        '',
        '--debug',
        dest='debug',
        help=SUPPRESS_HELP,
        action="store_true",
        default=False)
    parser.add_option('', '--proxy', dest='proxy', help=SUPPRESS_HELP)

    # pastebin-specific options first
    fpasteOrg_group = OptionGroup(parser, "fpaste.org Options")
    fpasteOrg_group.add_option(
        '-t',
        '--title',
        dest='title',
        help='title of paste; defaults to UNTITLED',
        metavar='"TITLE"')
    fpasteOrg_group.add_option(
        '-l',
        dest='lang',
        help='language of content for syntax highlighting; default is "%default"; use "list" to show all ' +
        str(
            len(validSyntaxOpts)) +
        ' supported langs',
        metavar='"LANGUAGE"')
    fpasteOrg_group.add_option(
        '-x',
        dest='expires',
        help='time before paste is removed; default is %default seconds for unauthenticated posts; valid options: ' +
        ', '.join(validExpiresOpts),
        metavar='EXPIRES')
    fpasteOrg_group.add_option(
        '-U',
        '--URL',
        help='URL of fpaste server; default is %default',
        dest='url',
        metavar='"FPASTE URL"')
    fpasteOrg_group.add_option(
        '-d',
        '--password',
        help='password for paste; default is %default',
        dest='password',
        metavar='"PASSWORD"')

    parser.add_option_group(fpasteOrg_group)
    # other options
    fpasteProg_group = OptionGroup(parser, "Input/Output Options")
    fpasteProg_group.add_option(
        '-i',
        '--clipin',
        dest='clipin',
        help='read paste text from current X clipboard selection [requires: xsel]',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '-o',
        '--clipout',
        dest='clipout',
        help='save returned paste URL to all available clipboards',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '',
        '--input-selection',
        dest='selection',
        help='specify which X clipboard to use. valid options: "primary" (default; middle-mouse-button paste), "secondary" (uncommon), or "clipboard" (ctrl-v paste)',
        metavar='CLIP')
    fpasteProg_group.add_option(
        '',
        '--fullpath',
        dest='fullpath',
        help='use pathname VS basename for file description(s)',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '',
        '--pasteself',
        dest='pasteself',
        help='paste this script itself',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '',
        '--sysinfo',
        dest='sysinfo',
        help='paste system information',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '',
        '--printonly',
        dest='printonly',
        help='print paste, but do not send',
        action="store_true",
        default=False)
    fpasteProg_group.add_option(
        '',
        '--confirm',
        dest='confirm',
        help='print paste, and prompt for confirmation before sending',
        action="store_true",
        default=False)
    parser.add_option_group(fpasteProg_group)

# Let default be anonymous.
#    p = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    (out, err) = p.communicate ()
#    if p.returncode == 0 and out:
#        user = out[0:-1]
#    else:
#        print >> sys.stderr, "WARNING Could not run whoami. Posting anonymously."

    parser.set_defaults(
        lang='text',
        expires='604800',
        selection='primary',
        password=None,
        url=FPASTE_URL)
    (options, args) = parser.parse_args()

    # Check for trailing slash
    if options.url[-1] != '/':
        options.url = options.url + '/'

    if options.lang.lower() == 'list':
        print('Valid language syntax options:')
        for opt in validSyntaxOpts:
            print(opt)
        sys.exit(0)
    if options.clipin:
        if not os.access('/usr/bin/xsel', os.X_OK):
            # TODO: try falling back to xclip or dbus
            parser.error(
                'OOPS - the clipboard options currently depend on "/usr/bin/xsel", which does not appear to be installed')
    if options.clipin and args:
        parser.error(
            "Sending both clipboard contents AND files is not supported. Use -i OR filename(s)")
    for optk, optv, opts in [('language', options.lang, validSyntaxOpts), ('expires', options.expires, validExpiresOpts), ('clipboard selection', options.selection, validClipboardSelectionOpts)]:
        if optv not in opts:
            parser.error(
                "'%s' is not a valid %s option.\n\tVALID OPTIONS: %s" %
                (optv, optk, ', '.join(opts)))

    fileargs = args
    if options.fullpath:
        fileargs = [os.path.abspath(x) for x in args]
    else:
        # remove potentially non-anonymous path info from file path
        # descriptions
        fileargs = [os.path.basename(x) for x in args]

    # guess lang for some common file extensions, if all file exts similar,
    # and lang not changed from default
    if options.lang == 'text':
        all_exts_similar = False
        ext_prev = ""
        for i in range(0, len(args)):
            all_exts_similar = True
            ext = os.path.splitext(args[i])[1].lstrip(os.extsep)
            if i > 0 and ext != ext_prev:
                all_exts_similar = False
                break
            ext_prev = ext
        if all_exts_similar and ext in list(ext2lang_map.keys()):
            options.lang = ext2lang_map[ext]

    # get input from mutually exclusive sources, though they *could* be
    # combined
    text = ""
    if options.clipin:
        xselcmd = 'xsel -o --%s' % options.selection
        # text = os.popen(xselcmd).read()
        p = subprocess.Popen(
            xselcmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (text, err) = p.communicate()
        text = text.decode("utf-8", "replace")
        if p.returncode != 0:
            if options.debug:
                print(err, file=sys.stderr)
            parser.error(
                "'xsel' failure. this usually means you're not running X")
        if not text:
            parser.error("%s clipboard is empty" % options.selection)
    elif options.pasteself:
        text = open(sys.argv[0]).read()
        options.lang = 'python'
    elif options.sysinfo:
        text = sysinfo(options.debug)
    elif not args:   # read from stdin if no file args supplied
        try:
            input_text = sys.stdin.buffer.read()
            text += input_text.decode("utf-8", "replace")
        except KeyboardInterrupt:
            print(
                "\nUSAGE REMINDER:\n   fpaste waits for input when run without file arguments.\n   Paste your text, then press <Ctrl-D> on a new line to upload.\n   Try `fpaste --help' for more information.\nExiting...",
                file=sys.stderr)
            sys.exit(1)
    else:
        for i, f in enumerate(args):
            if not os.access(f, os.R_OK):
                parser.error("file '%s' is not readable" % f)
            if (len(args) > 1):     # separate multiple files with header
                text += '#' * 78 + '\n'
                text += '### file %d of %d: %s\n' % (i+1,
                                                     len(args),
                                                     fileargs[i])
                text += '#' * 78 + '\n'
            text += open(f).read()
    if options.debug:
        print('lang: "%s"' % options.lang)
        print('text (%d): "%s ..."' % (len(text), text[:80]))

    if options.printonly or options.confirm:
        try:
            if is_text(text):
                # when piped to less, sometimes fails with [Errno 32] Broken
                # pipe
                print(text)
            else:
                print("DATA")
        except IOError:
            pass
    if options.printonly:   # print only what would be sent, and exit
        sys.exit(0)
    elif options.confirm:   # print what would be sent, and ask for permission
        if not confirm("OK to send?"):
            sys.exit(1)

    url = paste(text, options)
    if url:
        # Try to save URL in clipboard, and warn but don't throw error
        if options.clipout:
            if not os.access('/usr/bin/xsel', os.X_OK):
                print(
                    'OOPS - the clipboard options currently depend on "/usr/bin/xsel", which does not appear to be installed',
                    file=sys.stderr)
            else:
                # Copy the url in all the valid clipboard options
                for selection in validClipboardSelectionOpts:
                    xselcmd = 'xsel -i --%s' % selection
                    p = subprocess.Popen(
                        xselcmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE)
                    (out, err) = p.communicate(input=url.encode('utf-8'))
                    if p.returncode != 0:
                        if options.debug:
                            print(err, file=sys.stderr)
                        print(
                            "WARNING: URL not saved to %s" % selection,
                            file=sys.stderr)

        print(url)

    else:
        sys.exit(1)

    if options.pasteself:
        print(
            "install fpaste to local ~/bin dir by running:    mkdir -p ~/bin; curl " +
            url +
            "/raw -o ~/bin/fpaste && chmod +x ~/bin/fpaste",
            file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\ninterrupted.")
        sys.exit(1)
