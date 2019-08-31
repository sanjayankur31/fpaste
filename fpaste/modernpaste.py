"""
Modernpaste handler for fpaste

File: modernpaste.py

Copyright 2019 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import sys
import json
import time
import urllib
from fpaste.utils import is_text, confirm, USER_AGENT


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


