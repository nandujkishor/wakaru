import datetime, time, json, os, requests, uuid, urllib, adal
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

CLIENT_ID = '251a95e5-a120-4501-8c90-3915162fa9a6'
CLIENT_SECRET = ':DfKMEOfV=kjcdwjCdiaMaUQ/00q?L77'
# BASEURL = 'https://wakaru.amblygon.org'
BASEURL = 'http://localhost:8000'
RESOURCE = 'https://graph.microsoft.com'
API_VERSION = 'v1.0'
TENANT = 'am.amrita.edu'
AUTHORITY_URL = 'https://login.microsoftonline.com/' + TENANT
REDIRECT_URI = BASEURL + '/ad/response/'
AUTHORIZE_URL = 'https://login.microsoftonline.com/am.amrita.edu/oauth2/authorize?'+'response_type=code&client_id='+ CLIENT_ID +'&redirect_uri={}'+'&'+'state={}'

def sendtomicrosoft(request):
    if request.user.is_authenticated:
        messages.success(request, 'Already logged in!')
        return HttpResponseRedirect(BASEURL)
    auth_state = str(uuid.uuid4())
    return HttpResponseRedirect(AUTHORIZE_URL.format(BASEURL+reverse('ad:return'), auth_state))

def returnfrommicrosoft(request):
    code = request.GET['code']
    # print(code)
    auth_context = adal.AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, 'https://graph.microsoft.com', CLIENT_ID, CLIENT_SECRET)
    token = token_response['accessToken']
    print(token)
    http_headers = {'Authorization': 'Bearer ' + token,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    # print(http_headers)
    endpoint = RESOURCE + '/' + API_VERSION + '/me/'
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    print(graph_data)
    email = graph_data['mail']
    try:
        user = User.objects.filter(username=email).first()
    except Exception as e:
        print(e)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        user = User.objects.create_user(username=email, email=email, password='bullshit123', first_name=graph_data['displayName'].split()[0])
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')
    return HttpResponse(str(graph_data))

# @login_required
# def profilepicture(request):
