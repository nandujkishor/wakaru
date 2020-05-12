from django.db import models

FILE = (('P', 'PDF'), ('W', 'Word file'))

class Resource(models.Model):
    title = models.CharField('Title', max_length=500)
    course = models.ForeignKey('courses.course', on_delete=models.CASCADE)
    lecture = models.ForeignKey('courses.lecture', on_delete=models.CASCADE, null=True)
    # Lecture as null indicates general resource
    # kind = models.CharField