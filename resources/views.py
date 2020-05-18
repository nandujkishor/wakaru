import json, requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Resource
from .forms import ResourceForm
from courses.models import Course, Lecture
from preview_generator.manager import PreviewManager

cache_path = '/home/average/Projects/wakaru/media/preview'

@login_required
@csrf_exempt
def add(request, code, lecture):
    try: lecture = Lecture.objects.get(pk=lecture)
    except Exception as e: raise Http404
    if request.method != "POST": raise Http404()

    print(request.FILES)
    form = ResourceForm(request.POST, request.FILES)
    print(form)
    # print(form.errors)
    if form.is_valid():
        file = form.cleaned_data['file']
        resource = Resource(title=file.name, lecture=lecture, file=file)
        resource.save()
    else:
        return HttpResponse("error")
    manager = PreviewManager(cache_path, create_folder= True)
    print(resource.file.path)
    path_to_preview_image = manager.get_jpeg_preview(resource.file.path, page=0)
    resource.preview = path_to_preview_image.split('/')[-1]
    resource.save()
    
    return HttpResponseRedirect(reverse('courses:course', args=[code]))

def video(request):
    return HttpResponseRedirect("https://youtube.com")