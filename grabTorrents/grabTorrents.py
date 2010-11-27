#! /usr/bin/env python

import feedparser
import urllib, urllib2
import bencode

storageFolder = "/Users/mike/Downloads/Torrents/"

sources = {"isohunt" : "http://isohunt.com/js/rss/" + encShow + "?iht=3&noSL", "ezrss" : "http://ezrss.it/search/index.php?show_name=" + encShow + "&show_name_exact=false&mode=rss&direct", "btjunkie" : "http://btjunkie.org/rss.xml?query=" + encShow}
shows = ["South Park", "Futurama", "Its Always Sunny In Philadelphia", "30 Rock", "Mad Men", "Weeds", "The Office", "Sons Of Anarchy", "Dexter"]

for show in shows:
    encShow = urllib.pathname2url(show)
    feed = feedparser.parse(sources["ezrss"])
    print("**************************************************************")
    print("Show: " + show)
    print("======================")
    print("**************************************************************")
    print("    Title              : " + str(feed.entries[0].title))
    print("    Updated            : " + str(feed.entries[0].updated))
    print("    Updated (Parsed)   : " + str(feed.entries[0].updated_parsed))
    print("    Summary            : " + str(feed.entries[0].summary))
    print("    Link               : " + str(feed.entries[0].link))
    print("**************************************************************")
    #for episode in feed.entries:
        #print("Episode Title: " + episode.title)
        #fHandle = open(storageFolder + episode.title + ".torrent", "w")
        #try:
            #tempTorrent = urllib2.urlopen(episode.link)
        #except:
            #print "Couldn't Fetch Torrent: " + episode.title
        
        #fHandle.write(tempTorrent.read())
        #fHandle.close()
rawTorrent = open("test.torrent")
torrentData = rawTorrent.read()
rawTorrent.close()
decodedTorrent = bencode.bdecode(torrentData)
#Change file name, etc. in here...
newTorrent = bencode.bencode(decodedTorrent)
newTorrentFile = open("test_modified.torrent", "w")
newTorrentFile.write(newTorrent)
newTorrentFile.close()
