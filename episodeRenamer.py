#!/usr/bin/env python

import urllib2
import re
import os
import sys
import getopt

from tv.show import Show

VERSION = "0.1-dev"

SERIES_PARSER = [
    re.compile("^.*?s *(?P<series>\d+) *e *(?P<episode>\d+).*\.(?P<extension>.*?)$", re.IGNORECASE),
    re.compile("^.*?(?P<series>\d+)x(?P<episode>\d+).*\.(?P<extension>.*?)$", re.IGNORECASE),
    re.compile("^(?:.*?\D|)(?P<series>\d\{1,2\})(?P<episode>\d\{2\})(?:\D.*|)\.(?P<extension>.*?)$", re.IGNORECASE),
    ]
    
def get_page(page_url):
    try:
        return urllib2.urlopen(page_url).read()
    except urllib2.HTTPError, error:
        print "An HTTP error: %s." % error.code
        sys.exit()

def parse_epguides(showName = ""):
    """Parse an epguides page."""

    site = {"url": ["http://epguides.com/%s/"],
            "domain": "epguides.com",
            "urlparser": "epguides.com\/(.*?)\/",
           }

    page = get_page(site["url"][0] % showName)

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
    # Here is where there is a little bit of finesse needed for discarding characters that shouldn't be allowed in filenames...
    #new_filename = re.sub("[\\\:\*\"\?\<\>\|]", "", new_filename)
    # Allowed question marks in file names below
    new_filename = re.sub("[\\\:\*\"\<\>\|]", "", new_filename)
    
    return new_filename, info_dictionary

def rename_files(show = None, options = {}):
    allowableExtensions = [".avi", ".mpg", ".mov", ".mkv", ".mp4", ".m4v"]
    print("Allowable Extensions for Conversion: " + str(allowableExtensions))
    for filename in os.listdir(options["folder"]):
        extension = os.path.splitext(filename)[1]
        if extension in allowableExtensions: 
            try:
                new_filename, info_dictionary = parse_filename(show, filename, options["mask"])
            except:
                print 'Episode name for "%s" not found.' % filename
                continue

            print "Renaming \"%s\" to \"%s\"..." % (filename, new_filename.encode("ascii", "replace"))
            if options["preview"] == False:
                
                try:
                    os.rename(options["folder"] + "/" + filename, options["folder"] + "/" + new_filename)
                except Exception as (errno, strerror):
                    print("There was an error while renaming the file.")
                    print("Error({0}): {1}".format(errno, strerror))
        else:
            if options["verbose"] == True:
                print(str(filename) + " has extension: " + extension + " and was not processed")

def usage():
    print("""TV Episode Renamer - Usage:
    python ./episodeRenamer.py --title="SHOW TITLE" [other options]
    -h, --help           This help message
    -v, --verbose        Turn on verbose output
    -p, --preview        Don't actually rename files
    -m, --mask="MASK"    printf style string for renaming mask
      def: %(show)s - S%(series_num)02dE%(episode_num)02d - %(title)s.%(extension)s
    -t, --title="TITLE"  Sets the show title for the search
    """)

def main(parser = "epguides", verbose = False, preview = False, mask="%(show)s - S%(series_num)02dE%(episode_num)02d - %(title)s.%(extension)s", folder=".", title = ""):
    options = {
        "parser": parser,
        "verbose": verbose,
        "preview": preview,
        "mask": mask, 
        "folder": folder,
        "title": title
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvpm:f:t:", ["help", "verbose", "preview", "mask=", "folder=", "title="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--verbose"):
            print("Verbose output activated.")
            options["verbose"] = True
        elif o in ("-p", "--preview"):
            print("Preview mode activated.") 
            options["preview"] = True 
        elif o in ("-m", "--mask"):
            print("Non-Default Mask: " + a) 
            options["mask"] = a
        elif o in ("-f", "--folder"):
            print("Conversion Directory: " + a) 
            options["folder"] = a
        elif o in ("-t", "--title"):
            print("Show title: " + a)
            options["title"] = a
        else:
            print("o: " + o + ", a: " + a)
            assert False, "unhandled option"
    

    show = parse_epguides(options["title"])
    rename_files(show, options)
    
    print "Done."

if __name__ == "__main__":
    main()
