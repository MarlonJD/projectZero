from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserCreationForm, StatementForm
from panel.models import (Album, ContentID, Statistic, Track, Platform,
                          Statement, Genre)


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

    def get_queryset(self):
        return Statistic.objects.all().order_by('album')


def statisticAdminAddFunctionView(request):
    """
    Admin Statistic Add Function View
    """
    if request.method == 'POST':
        albumObj = Album.objects.get(pk=request.POST['album'])
        trackObj = Track.objects.get(pk=request.POST['track'])
        platformObj = Platform.objects.get(pk=request.POST['platform'])

        Statistic.objects.create(album=albumObj,
                                 track=trackObj,
                                 platform=platformObj,
                                 stream=request.POST['stream'],
                                 download=request.POST['download'],
                                 revenue=request.POST['revenue'],
                                 date=request.POST['date'])
        return redirect(reverse_lazy('secret:statistic'))
    else:
        albums = Album.objects.all()
        params = {'albums': albums, 'platforms': Platform.objects.all}
        return render(request, 'secret/statisticAdd.html', params)


class statementsAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Statement Page Class View: ListView
    """
    model = Statement
    template_name = 'secret/statement.html'
    fields = '__all__'

    def get_queryset(self):
        return Statement.objects.all().order_by('album')


class statementAdminCreateView(AdminStaffRequiredMixin, CreateView):
    """
    Admin, Statement Add Page Class View: CreateView
    """
    form_class = StatementForm
    success_url = reverse_lazy('secret:statement')
    template_name = 'secret/statementAdd.html'


class statementAdminUpdateView(AdminStaffRequiredMixin, UpdateView):
    """
    Admin, Statement Update Function, Class View: UpdateView
    """
    model = Statement
    fields = ['status', ]
    template_name = 'secret/contentID.html'
    success_url = reverse_lazy('secret:statement')


class statementAdminDeleteView(AdminStaffRequiredMixin, DeleteView):
    """
    Admin, Statement Delete Function, Class View: DeleteView
    """
    model = Statement
    template_name = 'secret/contentID.html'
    success_url = reverse_lazy('secret:statement')


class genreAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Genre Page Class View: ListView
    """
    model = Genre
    template_name = 'secret/genre.html'
    fields = '__all__'


class genreAdminCreateView(LoginRequiredMixin, CreateView):
    '''
    Panel, ContentID Request Page Class View
    '''
    success_url = reverse_lazy('secret:genre')
    template_name = 'secret/genreAdd.html'
    model = Genre
    fields = '__all__'

    # def form_valid(self, form):
    #    form.instance.user = self.request.user
    #    return super(contentIDUserRequestCreateView, self).form_valid(form)
