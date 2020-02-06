from django.views.generic import TemplateView, ListView, CreateView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import json
from datetime import timedelta, date
from panel.models import (Artist, Album, Genre, Platform, RecordLabel, Track,
                          ContentID, Statistic, Statement)
from panel.forms import ContentIDForm


class LabelUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Label, Label User permission mixin
    """
    def test_func(self):
        obj = RecordLabel.objects.filter(user=self.request.user)
        return obj


class indexLabelTemplateView(LabelUserRequiredMixin, TemplateView):
    """Label, Home Page (Dashboard) Page Class View: TemplateView
    """
    template_name = 'label/index.html'


class distLabelListView(LoginRequiredMixin, ListView):
    '''
    Panel, Distribution Page Class Based View: ListView
    '''
    model = Album
    template_name = 'label/distribution.html'
    # paginate_by = 50

    def get_queryset(self):
        try:
            recordObj = RecordLabel.objects.get(user=self.request.user)
        except RecordLabel.DoesNotExist:
            recordObj = None
        return Album.objects.filter(recordLabel=recordObj).order_by('-releaseDate')


@login_required
def addDistLabelView(request):
    '''
    Label, Add Distribution Page: Main Function View
    '''
    if request.method == 'POST':
        mType = request.POST['mType']
        title = request.POST['title']
        genre = request.POST['genre']
        releaseDate = request.POST['releaseDate']
        cover = request.FILES['cover']
        tracks = json.loads(request.POST['tracks'])
        recordLabel = request.POST['recordLabel']
        platforms = json.loads(request.POST['platforms'])

        genreObj = Genre.objects.get(pk=genre)

        try:
            recordObj = RecordLabel.objects.get(user=request.user)
        except RecordLabel.DoesNotExist:
            recordObj = RecordLabel.objects.create(name=recordLabel,
                                                   user=request.user)

        albumObj = Album.objects.create(mediaType=mType,
                                        title=title,
                                        artwork=cover,
                                        artist_label=request.POST['artist'],
                                        genre=genreObj,
                                        recordLabel=recordObj,
                                        releaseDate=releaseDate)

        for val in platforms:
            print(val)
            platObj = Platform.objects.get(pk=val)
            albumObj.platforms.add(platObj)

        for val in tracks:
            trackObj = Track.objects.get(pk=val['id'])
            albumObj.tracks.add(trackObj)

        return JsonResponse({"success": 1}, status=200)
    else:
        try:
            recordObj = RecordLabel.objects.get(user=request.user)
        except RecordLabel.DoesNotExist:
            recordObj = None

        twoWeekLater = date.today() + timedelta(days=15)

        return render(request, 'label/addDist.html',
                      {'platforms': Platform.objects.all,
                       'recordLabel': recordObj,
                       '2weekLater': twoWeekLater})


'''
---------------
ContentID Page
---------------
'''


class contentIDLabelListView(LoginRequiredMixin, ListView):
    '''
    Panel, ContentID Page Class Based View: ListView
    '''
    template_name = 'label/contentID.html'
    model = ContentID
    # paginate_by = 50

    def get_queryset(self):
        return ContentID.objects.filter(user=self.request.user)


class contentIDLabelRequestCreateView(LoginRequiredMixin, CreateView):
    '''
    Panel, ContentID Request Page Class View
    '''
    success_url = reverse_lazy('panel:contentID')
    template_name = 'label/contentIDRequest.html'
    form_class = ContentIDForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(contentIDLabelRequestCreateView, self).form_valid(form)


'''
---------------
Statistic Page
---------------
'''


class statisticLabelListView(LoginRequiredMixin, ListView):
    '''
    Label, Statistic Page Class Based View: ListView
    '''
    template_name = 'label/statistic.html'
    model = Statistic

    def get_queryset(self):
        recordObj = RecordLabel.objects.get(user=self.request.user)
        albumObj = Album.objects.filter(recordLabel=recordObj)
        return Statistic.objects.filter(album__in=albumObj)


'''
--------------
Statement Page
--------------
'''


class statementLabelListView(LoginRequiredMixin, ListView):
    '''
    Label, Statement Page Class Based View: ListView
    '''
    template_name = 'label/statement.html'
    model = Statement

    def get_queryset(self):
        recordObj = RecordLabel.objects.get(user=self.request.user)
        albumObj = Album.objects.filter(recordLabel=recordObj)
        return Statement.objects.filter(album__in=albumObj)
