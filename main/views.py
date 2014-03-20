# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Members
from .decorators import is_user_logged_in
from .helper import slice
import tweepy
import json


def home(request):
    return render(request, 'index.html')


def login(request):
    try:
        auth = tweepy.OAuthHandler(settings.TWITTER_OAUTH_CONSUMER_TOKEN, settings.TWITTER_OAUTH_CONSUMER_SECRET,
                                   settings.TWITTER_CALLBACK_URL)
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    except tweepy.TweepError:
        return HttpResponseBadRequest('401 - Unauthorized: Access is denied.')
    return HttpResponseRedirect(redirect_url)

@is_user_logged_in
def logout(request):
    try:
        del request.session['userId']
    except KeyError:
        pass
    return HttpResponseRedirect('/')


@is_user_logged_in
@require_POST
def post_ajax(request):
    responseData = {}
    if request.is_ajax():
        getUser = Members.objects.get(pk=request.session['userId'])
        jsonPost = json.loads(request.body)
        sliceItems = slice(jsonPost['tweet'], 140)
        try:
            auth = tweepy.OAuthHandler(settings.TWITTER_OAUTH_CONSUMER_TOKEN, settings.TWITTER_OAUTH_CONSUMER_SECRET)
            auth.set_access_token(getUser.access_token_key, getUser.access_token_secret)
            api = tweepy.API(auth)
            for item in sliceItems:
                api.update_status(item)
        except tweepy.TweepError:
            responseData['success'] = False
            responseData['message'] = 'Error!'
        responseData['success'] = True
        responseData['message'] = 'Your long tweet was successfully posted.'
    else:
        responseData['error'] = 'Ajax request aborted.'
    return HttpResponse(json.dumps(responseData), content_type="application/json")

@is_user_logged_in
def post(request):
    getUser = Members.objects.get(pk=request.session['userId'])
    return render_to_response('post.html', {'user': getUser }, context_instance=RequestContext(request))


def get_oauth(request):
    oauth_verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(settings.TWITTER_OAUTH_CONSUMER_TOKEN, settings.TWITTER_OAUTH_CONSUMER_SECRET)

    token = request.session['request_token']
    del request.session['request_token']

    auth.set_request_token(token[0], token[1])
    try:
        auth.get_access_token(oauth_verifier)
    except tweepy.TweepError:
        return HttpResponseBadRequest('Access token has expired and a refresh token is not available.')

    api = tweepy.API(auth)
    userinfo = api.me()

    try:
        getUserId = Members.objects.get(twitter_id=userinfo.id)
    except Members.DoesNotExist:
        getUserId = Members(twitter_screen_name=userinfo.screen_name,
                            twitter_fullname=userinfo.name,
                            twitter_id=userinfo.id,
                            profile_picture=userinfo.profile_image_url,
                            access_token_key=auth.access_token.key,
                            access_token_secret=auth.access_token.secret).save()
    else:
        Members.objects.filter(twitter_id=userinfo.id).update(twitter_screen_name=userinfo.screen_name,
                                                              twitter_fullname=userinfo.name,
                                                              profile_picture=userinfo.profile_image_url,
                                                              access_token_key=auth.access_token.key,
                                                              access_token_secret=auth.access_token.secret)
    request.session['userId'] = getUserId.id
    return HttpResponseRedirect('/post')
