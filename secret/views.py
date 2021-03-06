from django.views.generic import TemplateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserCreationForm, AnnoForm
from panel.models import (Album, ContentID, Statistic, Track, Platform,
                          Statement, SplitStatement, Genre, Announcement)


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


def distributionAdminDeleteView(request, pk):
    o = Album.objects.get(pk=pk)
    o.delete()

    return JsonResponse({'pk': pk, 'deleted': True})


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


@staff_member_required
def contentIDAdminDeleteView(request, pk):
    o = ContentID.objects.get(pk=pk)
    o.delete()

    return JsonResponse({'pk': pk, 'deleted': True})


class statisticAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Statistic Page Class View: ListView
    """
    model = Statistic
    template_name = 'secret/statistic.html'
    fields = '__all__'

    def get_queryset(self):
        return Statistic.objects.all().order_by('album')


@staff_member_required
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


@staff_member_required
def statisticAdminDeleteView(request, pk):
    o = Statistic.objects.get(pk=pk)
    o.delete()

    return JsonResponse({'pk': pk, 'deleted': True})


class statementsAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Statement Page Class View: ListView
    """
    model = Statement
    template_name = 'secret/statement.html'
    fields = '__all__'

    def get_queryset(self):
        return Statement.objects.all().order_by('album')


@staff_member_required
def statementAdminAddFunctionView(request):
    """
    Admin Statement Add Function View
    """
    if request.method == 'POST':
        albumObj = Album.objects.get(pk=request.POST['album'])

        # Create Statement Model Object
        stateObj = Statement.objects.create(album=albumObj,
                                            revenue=request.POST['revenue'],
                                            date=request.POST['date'])

        # Split Pays
        attributes = {}
        for k in request.POST.keys():
            if 'attr' in k:
                s = k.split('attr_')[1]
                attributes[s] = request.POST[k]
        for i in attributes:
            t = Track.objects.get(pk=i)
            sp = SplitStatement.objects.create(track=t, revenue=attributes[i],
                                               date=request.POST['date'])
            stateObj.splits.add(sp)

        return redirect(reverse_lazy('secret:statement'))
    else:
        albums = Album.objects.all()
        params = {'albums': albums}
        return render(request, 'secret/statementAdd.html', params)


class statementAdminUpdateView(AdminStaffRequiredMixin, UpdateView):
    """
    Admin, Statement Update Function, Class View: UpdateView
    """
    model = Statement
    fields = ['status', ]
    template_name = 'secret/contentID.html'
    success_url = reverse_lazy('secret:statement')


@staff_member_required
def statementAdminDeleteView(request, pk):
    o = Statement.objects.get(pk=pk)
    o.delete()
    return JsonResponse({'pk': pk, 'deleted': True})


class genreAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Genre Page Class View: ListView
    """
    model = Genre
    template_name = 'secret/genre.html'
    fields = '__all__'


class genreAdminCreateView(LoginRequiredMixin, CreateView):
    '''
    Admin, ContentID Request Page Class View
    '''
    success_url = reverse_lazy('secret:genre')
    template_name = 'secret/genreAdd.html'
    model = Genre
    fields = '__all__'


class annoAdminListView(AdminStaffRequiredMixin, ListView):
    """
    Admin, Announcement Page Class View: ListView
    """
    model = Announcement
    template_name = 'secret/anno.html'
    fields = '__all__'


class annoAdminCreateView(LoginRequiredMixin, CreateView):
    '''
    Admin, Announcement Request Page Class View
    '''
    success_url = reverse_lazy('secret:anno')
    template_name = 'secret/annoAdd.html'
    form_class = AnnoForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(annoAdminCreateView, self).form_valid(form)


@staff_member_required
def annoAdminDeleteView(request, pk):
    o = Announcement.objects.get(pk=pk)
    o.delete()

    return JsonResponse({'pk': pk, 'deleted': True})
