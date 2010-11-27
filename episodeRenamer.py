#!/usr/bin/env python

import urllib2
import optparse
import re
import os
import sys
import subprocess
import random

VERSION = "0.1-dev"

SERIES_PARSER = [
    re.compile("^.*?s *(?P<series>\d+) *e *(?P<episode>\d+).*\.(?P<extension>.*?)$", re.IGNORECASE),
    re.compile("^.*?(?P<series>\d+)x(?P<episode>\d+).*\.(?P<extension>.*?)$", re.IGNORECASE),
    re.compile("^(?:.*?\D|)(?P<series>\d\{1,2\})(?P<episode>\d\{2\})(?:\D.*|)\.(?P<extension>.*?)$", re.IGNORECASE),
    ]
    
class Show:
    def __init__(self, title=""):
        self.title = title
        self.attributes = {}
        self.episodes = {}

def get_page(page_url):
    try:
        return urllib2.urlopen(page_url).read()
    except urllib2.HTTPError, error:
        print "An HTTP error occurred, HTTP code %s." % error.code
        sys.exit()

def parse_epguides(show_id, options):
    """Parse an epguides page."""

    site = {"url": ["http://epguides.com/%s/"],
            "domain": "epguides.com",
            "urlparser": "epguides.com\/(.*?)\/",
           }

    page = get_page(site["url"][0] % show_id)

    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(page)
    page = unicode(soup).replace("\n", "")
    show = Show()
    try:
        show.title = re.search("""<h1><a href="http://.*?">(.*?)</a></h1>""", page).groups()[0]
    except AttributeError:
        print "Could not find show title, cannot continue."
        sys.exit()
    episodes = re.findall("\d+. +(?P<season>\d+) *\- *(?P<episode>\d+).*?<a.*?>(?P<name>.*?)</a>", page)
    for season, episode, name in episodes:
        show.episodes[(int(season), int(episode))] = {"title": name}
    return show

def parse_filename(show, filename, file_mask):
    for parser in SERIES_PARSER:
        matches = parser.search(filename)
        try:
            match_dict = matches.groupdict()
            break
        except AttributeError:
            continue
    else:
        raise Exception("Filename not matched.")

    series = int(match_dict["series"])
    episode = int(match_dict["episode"])
    extension = match_dict["extension"]

    info_dictionary = {"show": show.title,
                       "series_num": series,
                       "episode_num": episode,
                       "extension": extension}

    try:
        info_dictionary.update(show.episodes[(series, episode)])
        new_filename = file_mask % info_dictionary
    except KeyError:
        print 'Episode name for "%s" not found.' % filename
        raise Exception
    new_filename = re.sub("[\\\g\:\*\"\?\<\>\|]", "", new_filename)
    
    return new_filename, info_dictionary

def rename_files(show, file_mask, preview=False):
    for filename in os.listdir("."):
        try:
            new_filename, info_dictionary = parse_filename(show, filename, file_mask)
        except:
            print 'Episode name for "%s" not found.' % filename
            continue

        print "Renaming \"%s\" to \"%s\"..." % (filename, new_filename.encode("ascii", "replace"))
        if not preview:
            try:
                os.rename(filename, new_filename)
            except:
                print "There was an error while renaming the file."

def main():
    parser = optparse.OptionParser(usage="%prog [options]", version="Episode Renamer v%s\n" % VERSION)
    parser.add_option("-e",
                      "--use-epguides",
                      dest="use_epguides",
                      action="store_true",
                      help="use epguides.com")
    parser.add_option("-m",
                      "--mask",
                      dest="mask",
                      default="%(show)s - S%(series_num)02dE%(episode_num)02d - %(title)s.%(extension)s",
                      metavar="MASK",
                      action="store",
                      type="string",
                      help="the filename mask to use when renaming (default: \"%default\")")
    parser.add_option("-p",
                      "--preview",
                      dest="preview",
                      action="store_true",
                      help="don't actually rename anything")

    parser.set_defaults(preview=False)
    (options, arguments)=parser.parse_args()

    if len(arguments) != 1:
        parser.print_help()
        sys.exit(1)

    if options.use_epguides:
        parser = parse_epguides
    else:
        print ("You must choose a parsing option")
        sys.exit()

    show = parser(arguments[0], options)
    rename_files(show, options.mask, options.preview)
    print "Done."

if __name__ == "__main__":
    main()
