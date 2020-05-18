from django.db import models
from django.contrib.auth.models import User

TERMS = (('o', 'Odd / Autumn'), ('e', 'Even / Spring'))

class Department(models.Model):
    code = models.CharField('Code', unique=True, max_length=5)
    name = models.CharField('Name', max_length=30)

    def __str__(self):
        return self.code + " " + self.name

class Course(models.Model):
    code = models.CharField('Code', unique=True, max_length=10)
    title = models.CharField('Title', max_length=200)
    department = models.ForeignKey('department', on_delete=models.CASCADE)

    def __str__(self):
        return self.code + ": " + self.title

class Edition(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    desc = models.CharField('Description', max_length=5000)
    year = models.IntegerField('Year')
    students = models.ManyToManyField(User, related_name="student")
    instructors = models.ManyToManyField(User, related_name="instructor")
    term = models.CharField('Term', choices=TERMS, max_length=1)
    support = models.CharField('Support', max_length=1000, null=True)
    teams_url = models.CharField('Teams URL', max_length=1000, null=True, blank=True)
    piazza_url = models.CharField('Piazza URL', max_length=1000, null=True, blank=True)
    textbook_img = models.CharField('Textbook image', max_length=1000, null=True, blank=True)
    textbook_url = models.CharField('Textbook URL', max_length=1000, null=True, blank=True)
    textbook_title = models.CharField('Textbook title', max_length=100, null=True, blank=True)
    textbook_authors = models.CharField('Textbook authors', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.course.code + " " + str(self.year) + " " + self.get_term_display()

class Lecture(models.Model):
    class Meta:
        unique_together = ['edition', 'order']
    datetime = models.DateTimeField('datetime', null=True, blank=True)
    edition = models.ForeignKey('edition', on_delete=models.CASCADE)
    order = models.IntegerField('Order')
    title = models.CharField('Title', max_length=100)
    desc = models.CharField('Description', max_length=2000)
    tags = models.CharField('Tags', max_length=1000, null=True, blank=True)

    @classmethod
    def create(cls, edition):
        lastl = cls.objects.filter(edition=edition).order_by('-order').first()
        return cls(edition=edition, order=lastl.order+1, title="Click on the title to change", desc="Then type in a wonderful description for your students. Just double click on top of the content and then hit enter when you're done.")

    def __str__(self):
        return self.edition.course.code + " -- " + str(self.order) + ". " + self.title

# No topics for now
## All lectures are under a topic.
## A course has by default has a single topic.
## Topic display on read-mode requires atleast two topics