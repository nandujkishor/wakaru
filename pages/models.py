import hashlib
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Page(models.Model):
    title = models.CharField('Title', max_length=500)
    hash = models.CharField('Hash', max_length=500, unique=True)
    lecture = models.ForeignKey('courses.lecture', on_delete=models.CASCADE)
    pub_content_html = models.CharField('Content-HTML', max_length=100000)
    pub_content_delta = models.CharField('Content-Delta', max_length=100000)
    pub_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @classmethod
    def create(cls, lecture, user=None):
        page = cls(title="Lecture note", lecture=lecture, creator=user, pub_content_html="<p>Type ahead.</p>")
        page.save()
        page.hash = hashlib.sha224((str(lecture)+str(page.id)).encode()).hexdigest()
        page.save()
        return page

class Revision(models.Model):
    page = models.ForeignKey('page', on_delete=models.CASCADE)
    content_delta = models.CharField('Content-Delta', max_length=1000000)
    time = models.DateTimeField(default=timezone.now)
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @classmethod
    def create(cls, page, delta, user):
        return cls(page=page, content_delta=delta, editor=user)