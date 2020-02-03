from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from panel.models import Album, Track, Platform, Genre
from .serializers import GenreSerializer


class loadTracksAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        albumPK = self.kwargs['aid']

        # Sanity Check
        try:
            albumObj = Album.objects.get(pk=albumPK)
        except Album.DoesNotExist:
            return Response({'Error': _('Album does not exist')}, status=404)

        tracks = Track.objects.filter(tracks_set=albumObj)
        jResponse = [{'value': "", 'text': _('Please select an option')}, ]
        for track in tracks:
            jResponse.append({'text': track.name, 'value': track.pk})

        return Response(jResponse)


class loadPlatformsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        albumPK = self.kwargs['aid']

        # Sanity Check
        try:
            albumObj = Album.objects.get(pk=albumPK)
        except Album.DoesNotExist:
            return Response({'Error': _('Album does not exist')}, status=404)

        tracks = Platform.objects.filter(platforms_set=albumObj)
        jResponse = [{'value': "", 'text': _('Please select an option')}, ]
        for track in tracks:
            jResponse.append({'text': track.name, 'value': track.pk})

        return Response(jResponse)


class GenreViewSet(ModelViewSet):
    """
    List genres from Rest API
    """
    model = Genre
    serializer_class = GenreSerializer
    permission_classes = [IsLoggedInUserOrAdmin]

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            if (obj.subgenres.all()):
                data['children'] = self.serialize_tree(obj.subgenres.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset().filter(parent=None)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        self.object = self.get_object()
        data = self.serialize_tree([self.object])
        return Response(data)

    def get_queryset(self):
        return Genre.objects.all()


@staff_member_required
def addGenre(request):
    jsonBody = json.loads(request.body)
    try:
        parent = Genre.objects.get(pk=jsonBody['parent'])
    except Genre.DoesNotExist:
        parent = None
    except KeyError:
        parent = None

    name = jsonBody['name']

    try:
        Genre.objects.create(parent=parent,
                             name=name)
    except:
        return JsonResponse({
            "ErrorCode": 2,
            "Message": "Genre could not inserted for some reason Try again or please contact the IT"})
    finally:
        return JsonResponse({
            "SuccessCode": 1,
            "Message": "Genre Inserted"})


@staff_member_required
def removeGenre(request):
    try:
        jsonBody = json.loads(request.body)
        id = jsonBody['cat']
        c = Genre.objects.get(pk=id)
        c.delete()

        return JsonResponse({
            "SuccessCode": 1,
            "Message": "Category Removed"})
    except:
        return JsonResponse({
            "FailedCode": 1,
            "Message": "Dont know why but there is a issue"}, status=418)


class getSplitPays(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        albumPK = self.kwargs['aid']

        # Sanity Check
        try:
            albumObj = Album.objects.get(pk=albumPK)
        except Album.DoesNotExist:
            return Response({'Error': _('Album does not exist')}, status=404)

        trackCount = Track.objects.filter(tracks_set=albumObj).count()
        splitPays = Track.objects.filter(tracks_set=albumObj).exclude(
            OtherArtists__isnull=True)
        jResponse = []
        for t in splitPays:
            jResponse.append({'count': trackCount, 'id': t.pk, 'name': t.name})

        return Response(jResponse)
