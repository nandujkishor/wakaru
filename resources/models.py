from django.db import models

FILE = (('PDF', 'Portable Document Format'), ('DOC', 'Word file'))

class Resource(models.Model):
    title = models.CharField('Title', max_length=500)
    # course = models.ForeignKey('courses.course', on_delete=models.CASCADE)
    lecture = models.ForeignKey('courses.lecture', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='uploads/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Lecture as null indicates general resource
    extension = models.CharField(choices=FILE, max_length=3, null=True)
    comment = models.CharField(max_length=1000, null=True)
    preview = models.CharField(max_length=1000, null=True)