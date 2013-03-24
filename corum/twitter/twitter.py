import datetime
import urllib2
import json


class Twitter:

    username = None
    FRIENDS_URL = "https://api.twitter.com/1/statuses/friends/%s.json"
    STATUS_URL = "https://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&count=%d"
    PROFILE_URL = "https://api.twitter.com/1/users/show.json?screen_name=%s"

    def __init__(self, username):
        self.username = username

    def get_friends(self):
        friends = []
        for friend in self._request(self.FRIENDS_URL % (self.username)):
            friends.append(User._init_with_dict(friend))
        return friends

    def get_statuses(self, count=100):
        statuses = []
        for status in self._request(self.STATUS_URL % (self.username, count)):
            statuses.append(Status._init_with_dict(status))
        return statuses

    def get_profile(self):
        return User._init_with_dict(self._request(self.PROFILE_URL % (self.username)))

    def _request(self, url):
        return json.load(urllib2.urlopen(url))


class User:
    name = None
    username = None
    description = None
    location = None
    url = None
    picture = None
    followers = None
    following = None
    statuses = None
    status = None
    last_location = None

    @classmethod
    def _init_with_dict(cls, dictionary):
        user = cls()
        user.name = dictionary["name"]
        user.username = dictionary["screen_name"]
        user.description = dictionary["description"]
        user.location = dictionary["location"]
        user.url = dictionary["url"]
        user.picture = dictionary["profile_image_url"]
        user.followers = dictionary["followers_count"]
        user.following = dictionary["friends_count"]
        user.statuses = dictionary["statuses_count"]

        if "status" in dictionary:
            user.status = Status._init_with_dict(dictionary["status"])
        return user

    def __str__(self):
        return self.username


class Status:
    date = None
    text = None
    location = None

    @classmethod
    def _init_with_dict(cls, dictionary):
        status = cls()
        status.date = datetime.datetime.strptime(dictionary["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
        status.text = dictionary["text"]

        if ("coordinates" in dictionary and
                dictionary["coordinates"] is not None):
            status.location = {}
            status.location['lat'] = dictionary["coordinates"]["coordinates"][1]
            status.location['long'] = dictionary["coordinates"]["coordinates"][0]
            print status.location
        return status
