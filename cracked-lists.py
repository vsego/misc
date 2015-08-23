#!/usr/bin/env python3

"""
A program to retrieve [Cracked](http://www.cracked.com/)'s list-articles
and display only their headers.

Intended for fast backreading from RSS and similar collections of links.

@Author: Vedran Sego <vsego@vsego.org>
"""

from html.parser import HTMLParser
import urllib.request
from pprint import pprint

class CrackedListHTMLParser(HTMLParser):
    """
    The list parser, looking for `h1`, `h2.subheading`, and `a.next` tags.
    """
    first = True        # Is this the first page or did we get here by following a "next" link?
    print_data = False  # Should the data be printed?
    followups = list()  # The list of links to follow
    current = list()    # The current title/item (in case it is broken by other tags)
    def handle_starttag(self, tag, attrs):
        """
        Handles the start of `h1` (the main title),
        `h2.cubheading` (section headers),
        and `a.next` (link to the next page).
        """
        attrs = dict(attrs)
        if (tag == "h1" and self.first) or \
           (tag == "h2" and attrs.get("class") == "subheading"):
            self.print_data = True
            self.current = list()
        if tag == "a" and attrs.get("class") == "next" and "href" in attrs:
            self.followups.append(attrs["href"])
    def handle_endtag(self, tag):
        """
        Handles end tags (basically, wrap up the data collection).
        """
        if self.print_data and tag in {"h1", "h2"}:
            self.print_data = False
            print(" ".join(self.current))
    def handle_data(self, data):
        """
        Collects the data that is inside the title tags.
        """
        if self.print_data:
            self.current.append(data.strip())
    def run(self, url = None):
        """
        Runs the parser. If `url` is given, it is used as a starting link.
        """
        if url is not None:
            self.followups = [ url ]
        self.first = True
        while True:
            urls = self.followups
            if not urls: break
            self.followups = list()
            for url in urls:
                with urllib.request.urlopen(url) as f:
                    self.feed(f.read().decode())
            self.first = False

parser = CrackedListHTMLParser()

while True:
    url = input("\nURL (empty to quit): ")
    if not url:
        break
    print()
    parser.run(url)
