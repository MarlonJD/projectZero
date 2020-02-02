from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from panel.models import (Album, ContentID, Statistic, Track, Platform,
                          Statement, Genre, RecordLabel)


class LabelUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Label, Label User permission mixin
    """
    def test_func(self):
        obj = RecordLabel.objects.filter(user=self.request.user)
        return obj


class indexLabelTemplateView(LabelUserRequiredMixin, TemplateView):
    """
    Admin, Home Page (Dashboard) Page Class View: TemplateView
    """
    template_name = 'label/index.html'
