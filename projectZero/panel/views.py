from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Album, Artist


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
