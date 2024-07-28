from django import forms
from . import models

class audioForm(forms.ModelForm):
    class Meta():
        model = models.Entries
        fields = ('audio_file',)