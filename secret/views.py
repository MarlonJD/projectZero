from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCreationForm
from panel.models import (Album, ContentID, Statistic)


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Admin, Admin permission mixin
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class indexAdminTemplateView(AdminStaffRequiredMixin, TemplateView):
    """
    Admin, Home Page (Dashboard) Page Class View: TemplateView
    """
    template_name = 'secret/index.html'


class distributionAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Distribution Page Class View: ListView
    """
    template_name = 'secret/distribution.html'
    model = Album

    def get_queryset(self):
        return Album.objects.all().order_by('status')


class distributionAdminDetailView(AdminStaffRequiredMixin, DetailView):
    """
    Admin, Distribution Detail Page Class View: DetailView
    """
    template_name = 'secret/distDetail.html'
    model = Album


class distributionAdminUpdateView(AdminStaffRequiredMixin, UpdateView):
    """
    Admin, Distribution Update Function, Class View: UpdateView
    """
    model = Album
    fields = ['status', ]
    template_name = 'secret/distDetail.html'
    success_url = reverse_lazy('secret:distribution')


class distributionAdminDeleteView(AdminStaffRequiredMixin, DeleteView):
    """
    Admin, Distribution Delete Function, Class View: DeleteView
    """
    model = Album
    template_name = 'secret/distribution.html'
    success_url = reverse_lazy('secret:distribution')


class userAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, User Page Class View: ListView
    """
    template_name = 'secret/user.html'
    model = User
    fields = ['username', 'email', ]


class userSignUpAdminCreateView(AdminStaffRequiredMixin, CreateView):
    """
    Admin, User SignUp Page Class View: CreateView
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('secret:user')
    template_name = 'secret/userRegister.html'


class contentIDAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, contentID Page Class View: ListView
    """
    template_name = 'secret/contentID.html'
    model = ContentID
    fields = '__all__'


class contentIDAdminUpdateView(AdminStaffRequiredMixin, UpdateView):
    """
    Admin, contentID Update Function, Class View: UpdateView
    """
    model = ContentID
    fields = ['status', ]
    template_name = 'secret/contentID.html'
    success_url = reverse_lazy('secret:contentID')


class contentIDAdminDeleteView(AdminStaffRequiredMixin, DeleteView):
    """
    Admin, ContentID Delete Function, Class View: DeleteView
    """
    model = ContentID
    template_name = 'secret/contentID.html'
    success_url = reverse_lazy('secret:contentID')


class statisticAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Statistic Page Class View: ListView
    """
    model = Statistic
    template_name = 'secret/statistic.html'
    fields = '__all__'