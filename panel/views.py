from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Album, Artist, Track, Platform
import json


@login_required
def indexView(request):
    return render(request, 'panel/index.html')


@login_required
def distView(request):
    artistObj = Artist.objects.get(user=request.user)
    distsObj = Album.objects.filter(artist=artistObj).order_by('-releaseDate')
    params = {'dists': distsObj}
    return render(request, 'panel/distribution.html', params)


@login_required
def adddistUserView(request):
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
        return render(request, 'panel/addDist.html', {'platforms': Platform.objects.all})


@login_required
# Distribution Track Add: Media Uploader
def trackUpload(request):
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
