import urllib2
import json


class Twitter(object):

    username = None
    FRIENDS_URL = "https://api.twitter.com/1/statuses/friends/%s.json"
    STATUS_URL = "https://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&count=%d"

    def __init__(self, username):
        self.username = username

    def get_friends(self):
        return self._request(self.FRIENDS_URL % (self.username))

    def get_statuses(self, count):
        return self._request(self.STATUS_URL % (self.username, count))

    def _request(self, url):
        return json.load(urllib2.urlopen(url))



class User(object):
    name = None
    username = None
    description = None
    location = None
    url = None
    picture = None
    followers = None
    following = None
    statuses = None

    def __init__(self, dictionary):
        self.name = dictionary["name"]
        self.username = dictionary["screen_name"]
        self.description = dictionary["description"]
        self.location = dictionary["location"]
        self.url = dictionary["url"]
        #TODO ... Change this to a file object
        self.picture = dictionary["profile_image_url"]
        self.followers = dictionary["followers_count"]
        self.following = dictionary["friends_count"]
        self.statuses = dictionary["statuses_count"]

