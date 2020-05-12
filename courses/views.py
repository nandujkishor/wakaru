from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Lecture, Edition
from pages.models import Page

@login_required
def home(request):
    courses = Course.objects.all()
    return render(request, "home.html", {'user':request.user, 'courses':courses})

@login_required
def course(request, code):
    try: course = Course.objects.get(code=code.upper())
    except Exception as e: raise Http404

    # courses = Course.objects.filter(edition__students=request.user).all()
    courses = Course.objects.all()

    edition = course.edition_set.filter(course=course, year=2020, term='e').first()
    lectures = Lecture.objects.filter(edition=edition).all()
    # Temp: for this semester only

    if edition.instructors.filter(pk=request.user.id):
        instructor = True
        # courses = Course.objects.filter(edition__instructors=request.user).all()
    else: instructor = False

    return render(request, "course_home.html", {'course':course, 'courses':courses, 'lectures':lectures, 'user':request.user, 'instructor':instructor})

def addpage(request, code, lecture):
    try: course = Course.objects.get(code=code.upper())
    except Exception as e: raise Http404

    edition = course.edition_set.filter(course=course, year=2020, term='e').first()
    lecture = Lecture.objects.get(pk=lecture)

    page = Page.create(lecture)
    return HttpResponseRedirect(reverse('pages:editor', args=[page.hash]))

def viewpage(request, code, lecture, hash, title, id):
    try: page = Page.objects.get(pk=id)
    except Exception as e: raise Http404

    return render(request, "view_page.html", {'page':page})

@csrf_exempt
def editlecture(request, code, lecture, content):
    try: course = Course.objects.get(code=code.upper())
    except Exception as e: raise Http404
    if request.method != "POST": raise Http404
    edition = course.edition_set.filter(course=course, year=2020, term='e').first()
    lecture = Lecture.objects.get(pk=lecture)

    newc = request.POST['data']
    print(newc)
    if content == "title": lecture.title = newc
    elif content == "desc": lecture.desc = newc
    lecture.save()

    return JsonResponse({'success':'true'})

def newlecture(request, code):
    try: course = Course.objects.get(code=code.upper())
    except Exception as e: raise Http404

    edition = course.edition_set.filter(course=course, year=2020, term='e').first()
    newl = Lecture.create(edition)
    newl.save()

    if edition.instructors.filter(pk=request.user.id):
        instructor = True
        courses = Course.objects.filter(edition__instructors=request.user).all()
    else: instructor = False

    return render(request, "lecture.html", {'lecture':newl, 'instructor':instructor})
