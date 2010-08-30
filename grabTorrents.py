import feedparser
import urllib, urllib2

storageFolder = "/Users/mike/Downloads/Torrents/"

shows = ["South Park", "Futurama"]

for show in shows:
    encShow = urllib.pathname2url(show)
    feed = feedparser.parse("http://ezrss.it/search/index.php?show_name=" + encShow + "&show_name_exact=false&mode=rss&direct")
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
