from django import forms

class UploadFileForm(forms.Form):
    text = forms.FileField()