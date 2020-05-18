from django import forms

class ResourceForm(forms.Form):
    file = forms.FileField()