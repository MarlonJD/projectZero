from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContentID


class ContentIDForm(forms.ModelForm):
    class Meta:
        model = ContentID
        fields = ['title', 'url']
        labels = {
            'title': _('Title'),
            'url': _('URL')
        }
