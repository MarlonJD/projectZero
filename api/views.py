from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from panel.models import Album, Track, Platform


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
