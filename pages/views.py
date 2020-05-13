import json, requests
from delta import html
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Page, Revision

@login_required
def editor(request, hash):
    page = Page.objects.filter(hash=hash).first()
    if page is None: raise Http404()

    try: fact = requests.get('http://numbersapi.com/random/trivia')
    except Exception as e: fact = "Oops. Our trivia engine is suffering a heart attack."

    if fact.status_code != '200': fact = "Oops. Our trivia engine is suffering a heart attack."
    else: fact = fact.text

    return render(request, "editor.html", {'page':page, 'fact':fact})

@login_required
@csrf_exempt
def save(request, hash):
    if request.method != 'POST': raise Http404()
    page = Page.objects.filter(hash=hash).first()
    if page is None: raise Http404()
    
    # print(request.POST)
    # print("two")
    # print(request.POST['doc'])
    # print("Delta")
    delta = json.loads(request.POST['doc'])['ops']
    revision = Revision.create(page, delta, request.user)
    revision.save()

    # Temporarily: since no drafts right now
    page.pub_content_delta = delta
    page.pub_content_html = html.render(delta)
    page.pub_time = timezone.now()
    page.save()

    print(page.pub_content_html)
    
    return JsonResponse({'success':'true'})