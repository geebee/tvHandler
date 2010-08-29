import feedparser
import urllib2

storageFolder = "/Users/mike/Downloads/Torrents/"

#South Park Episodes
feed = feedparser.parse("http://ezrss.it/search/index.php?show_name=South+Park&show_name_exact=false&mode=rss&direct")
for episode in feed.entries:
    print("Episode Title: " + episode.title)
    #fHandle = open(storageFolder + episode.title + ".torrent", "w")
    #try:
        #tempTorrent = urllib2.urlopen(episode.link)
    #except:
        #print "Couldn't Fetch Torrent: " + episode.title
    
    #fHandle.write(tempTorrent.read())
    #fHandle.close()
