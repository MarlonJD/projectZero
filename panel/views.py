from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Album, Artist, Track
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
    return render(request, 'panel/addDist.html')


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
