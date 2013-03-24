# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from models import TwitterCase
from core.models import Location


def case(request, twitter_case_id):
    case = TwitterCase.objects.get()
    data = serializers.serialize("json", list(case.twitter_user.tweet_set.all()) + list(Location.objects.all()))
    return HttpResponse(data)
