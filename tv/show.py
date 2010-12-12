from episode import Episode

class Show (object):
    id = None
    title = ""
    actors = []
    attributes = {}
    episodes = {}

    def getShowById (self, showId = None):
        pass
    def getShowByName (self, showName = ""):
        pass
    def getShowByActors (self, actorsNames = []):
        pass
    def getAllEpisodes (self):
        pass
    def getSeason (self, seasonNumber = 0):
        pass
    def getSingleEpisode (self, episodeDict = {"s":0, "e":0}, episodeId = 0):
        pass
