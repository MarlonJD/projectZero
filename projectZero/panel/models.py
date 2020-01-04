from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings

'''
-----------------------------
    Distribution Models
-----------------------------
Artist, OtherArtist, Partner,
RecordLabel, Track, Album
-----------------------------
'''


# Artist is Artist(name=String)
# interp. Main Artist of the media
#         user is User as artist's usership
#         name is the main artist name of media       String
#         appleArtist, spotifyArtist is the URL
class Artist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='artist_set')
    name = models.CharField(max_length=100, null=True)
    appleArtist = models.URLField(null=True)
    spotifyArtist = models.URLField(null=True)

    def __str__(self):
        return self.name


# OtherArtist is OtherArtist(name=String, rate=Interval[0,100])
# interp. Other artist of the media.
#         artist is the Artist                        Artist
#         rate is the split pay rate of the media     Interval[0,100]
class OtherArtist(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return self.artist.name + ' ' + str(self.rate) + '%'


# Platform is Platform(name=String)
# interp. Platform of the that media will share in
#         id is the primary key that automaticly
#            given and use as enumatation
#         name is the partner's name                 String
class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# RecordLabel is RecordLabel(user=User, name=String)
# interp. RecordLabel is the label company for media
#         user is the label company user (if any)
#         name is the label name
class RecordLabel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=100)


# Track is Track(media=FILE)
# interp. track is the media file
#         media is the FILE
#         otherArtists is OtherArtist for split paying
class Track(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=150)
    media = models.FileField(upload_to='media')
    OtherArtists = models.ManyToManyField(OtherArtist,
                                          related_name='otherArtists_set')


# Album is Album(title=String, artist=Artist,
#                genre=String, subgenre=String,
#                appleArtist=URL, spotifyArtist=URL,
#                recordLabel=String, releaseDate=Date,
#                partners=Partner, OtherArtists=OtherArtist)
# interp. Album ia music or music video or any media
#         mediaType is MediaType Choices
#         tracks is Track list
#         title is the media's title
#         artwork is the album cover image
#         artist is the media's Artist
#         genre, subgenre is the media's genre
#         partners is Partner
class Album(models.Model):

    class mediaType(models.IntegerChoices):
        SINGLE = 0, _('Single')
        EP = 1, _('EP')
        ALBUM = 2, _('Album')
        __empty__ = _('Please Select...')

    mediaType = models.IntegerField(choices=mediaType.choices)
    tracks = models.ManyToManyField(Track,
                                    related_name='tracks_set')
    title = models.CharField(max_length=150)
    artwork = models.ImageField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    subgenre = models.CharField(max_length=50, null=True)
    recordLabel = models.CharField(max_length=150)
    releaseDate = models.DateField()
    platforms = models.ManyToManyField(Platform,
                                       related_name='partners_set')

    def __str__(self):
        return self.title + ' by ' + self.artist.name


'''
-----------------------------
    Content ID Model
-----------------------------
         ContentID
-----------------------------
'''


# ContentID is ContentID(title=String, url=URL, status=statusType Choices)
# interp. ContentID is Youtube removal request
#         title is the Media's title
#         url is media's URL
#         status is statusType
class ContentID(models.Model):

    class statusType(models.IntegerChoices):
        PENDING = 0, _('Pending')
        RECIEVED = 1, _('Removal Request Received')
        __empty__ = _('Please Select...')

    title = models.CharField(max_length=200)
    url = models.URLField()
    status = models.IntegerField(choices=statusType.choices)


'''
-----------------------------
     Statistic Models
-----------------------------
     Statistic, Statement
-----------------------------
'''


# Statistic is Statistic(track=Track, Platform, stream=Integer,
#                        download=Integer, revenue=Integer)
# interp. Statistic is Track's statistic
#         track is track with statistic
#         platform is Platform
#         stream is the stream count of media on that platform
#         revenue is the money comes from platform
class Statistic(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    stream = models.IntegerField()
    download = models.IntegerField()
    revenue = models.IntegerField()
