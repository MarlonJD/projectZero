from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .models import (Album, Artist, Track, Platform,
                     ContentID, Statistic)
import json


class indexUserTemplateView(LoginRequiredMixin, TemplateView):
    '''
    Panel Home Page (Dashboard) Page Class View
    '''
    template_name = "panel/index.html"


'''
---------------
Distribution Page
---------------
'''


class distUserListView(LoginRequiredMixin, ListView):
    '''
    Panel, Distribution Page Class Based View: ListView
    '''
    model = Album
    template_name = 'panel/distribution.html'
    # paginate_by = 50

    def get_queryset(self):
        try:
            artistObj = Artist.objects.get(user=self.request.user)
        except Artist.DoesNotExist:
            artistObj = None
        return Album.objects.filter(artist=artistObj).order_by('-releaseDate')


@login_required
def addDistUserView(request):
    '''
    Panel, Add Distribution Page: Main Function View
    '''
    if request.method == 'POST':
        try:
            mType = request.POST['mType']
            title = request.POST['title']
            artist = request.POST['artist']
            genre = request.POST['genre']
            subGenre = request.POST['subGenre']
            recordLabel = request.POST['recordLabel']
            releaseDate = request.POST['releaseDate']
            cover = request.FILES['cover']
            tracks = json.loads(request.POST['tracks'])
            platforms = json.loads(request.POST['platforms'])

            artistObj = Artist.objects.get_or_create(user=request.user,
                                                     name=artist)[0]

            albumObj = Album.objects.create(mediaType=mType,
                                            title=title,
                                            artwork=cover,
                                            artist=artistObj,
                                            genre=genre,
                                            subgenre=subGenre,
                                            recordLabel=recordLabel,
                                            releaseDate=releaseDate)

            for val in platforms:
                print(val)
                platObj = Platform.objects.get(pk=val)
                albumObj.platforms.add(platObj)
                
            for val in tracks:
                trackObj = Track.objects.get(pk=val['id'])
                albumObj.tracks.add(trackObj)
                
            return JsonResponse({"success": 1}, status=200)
        except:
            JsonResponse({"Message": "Couldn't add distribution for some reason"}, status=418)
    else:
        try:
            artistObj = Artist.objects.get(user=request.user)
        except Artist.DoesNotExist:
            artistObj = None
        
        return render(request, 'panel/addDist.html', {'platforms': Platform.objects.all,
                                                      'artist': artistObj})


@login_required
def trackUploadUser(request):
    '''
    Panel, Add Distribution Page: Media (Track) Uploader Helper Function
    '''
    try:
        number = request.POST['number']
        name = request.POST['name']
        t = Track.objects.create(number=number,
                                 name=name,
                                 media=request.FILES['media'])
        return JsonResponse({"id": t.id,
                             "number": '#' + str(t.number),
                             "name": t.name,
                             "fileName": t.media.name,
                             "url": t.media.url,
                             "size": str(round((t.media.size / 1048576), 2)) + ' MB'},
                            status=200)
    except:
        return JsonResponse({
            "FailedCode": 0,
            "Message": "Couldn't upload media for some reason"}, status=418)


'''
---------------
ContentID Page
---------------
'''


class contentIDUserListView(LoginRequiredMixin, ListView):
    '''
    Panel, ContentID Page Class Based View: ListView
    '''
    template_name = 'panel/contentID.html'
    model = ContentID
    # paginate_by = 50

    def get_queryset(self):
        return ContentID.objects.filter(user=self.request.user)


class contentIDUserRequestCreateView(LoginRequiredMixin, CreateView):
    '''
    Panel, ContentID Request Page Class View
    '''
    success_url = reverse_lazy('panel:contentID')
    template_name = 'panel/contentIDRequest.html'
    model = ContentID
    fields = ('title', 'url')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(contentIDUserRequestCreateView, self).form_valid(form)


'''
---------------
Statistic Page
---------------
'''


class statisticUserListView(LoginRequiredMixin, ListView):
    '''
    Panel, Statistic Page Class Based View: ListView
    '''
    template_name = 'panel/statistic.html'
    model = Statistic

    def get_queryset(self):
        artistObj = Artist.objects.get(user=self.request.user)
        albumObj = Album.objects.filter(artist=artistObj)
        return Statistic.objects.filter(album__in=albumObj)
