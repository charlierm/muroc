from django.db import models
from core.models import AbstractBase, Case, Location
from django.contrib.contenttypes import generic
from django.conf import settings
import threading
import twitter


class TwitterCase(AbstractBase):
    case = models.ForeignKey(Case)
    username = models.CharField(max_length=15)
    date_raised = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    twitter_user = models.OneToOneField('TwitterUser', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.twitter_user:
            self.fetch()
        super(TwitterCase, self).save(*args, **kwargs)

    def fetch(self):
        threading.Thread(target=self._fetch).start()

    def _clean(self):
        self.twitter_user.delete()

    def _fetch(self):
        self._fetch_profile()
        self._fetch_statuses()
        self._fetch_followers()

    def _fetch_followers(self):
        t = twitter.Twitter(self.username)
        friends = t.get_friends()

        for friend in friends:
            user = TwitterUser()
            user.name = friend.name
            user.username = friend.username
            user.description = friend.description
            user.url = friend.url
            user.followers = friend.followers
            user.following = friend.following
            user.statuses = friend.statuses
            user.save()

    def _fetch_statuses(self):
        t = twitter.Twitter(self.username)
        statuses = t.get_statuses()
        for status in statuses:
            tweet = Tweet()
            tweet.date = status.date
            tweet.text = status.text
            tweet.user = self.twitter_user
            if status.location:
                location = Location()
                location.latitude = status.location['lat']
                location.longitude = status.location['long']
                location.location_object = tweet
                location.save()
            tweet.save()

    def _fetch_profile(self):
        t = twitter.Twitter(self.username)
        friend = t.get_profile()
        user = TwitterUser()
        user.name = friend.name
        user.username = friend.username
        user.description = friend.description
        user.url = friend.url
        user.followers = friend.followers
        user.following = friend.following
        user.statuses = friend.statuses
        user.save()
        self.twitter_user = user
        self.save()


class Tweet(AbstractBase):
    date = models.DateField()
    text = models.CharField(max_length=140)
    location = generic.GenericRelation(Location, null=True, blank=True)
    user = models.ForeignKey('TwitterUser')

    def __unicode__(self):
        return self.text[0:20]

    class Meta:
        ordering = ["-date"]


class TwitterUser(AbstractBase):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=15)
    description = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(max_length=250, null=True, blank=True)
    picture = models.ImageField(upload_to='twitter', null=True, blank=True)
    followers = models.IntegerField()
    following = models.IntegerField()
    statuses = models.IntegerField()
    status = models.ForeignKey(Tweet, null=True, blank=True)

    def __unicode__(self):
        return self.username