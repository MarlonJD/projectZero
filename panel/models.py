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


class Artist(models.Model):
    """
    Artist is Artist(user=request.user, name=String)
    interp. Main Artist of the media
            user is User as artist's usership
            name is the main artist name of media       String
            appleArtist, spotifyArtist is the URL
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='artist_set')
    name = models.CharField(max_length=100, null=True)
    appleArtist = models.URLField(null=True, blank=True)
    spotifyArtist = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class OtherArtist(models.Model):
    """
    OtherArtist is OtherArtist(name=String, rate=Interval[0,100])
    interp. Other artist of the media.
            artist is the Artist                        Artist
            rate is the split pay rate of the media     Interval[0,100]
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='otherartist_set')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return self.artist.name + ' ' + str(self.rate) + '%'


class Platform(models.Model):
    """
    Platform is Platform(name=String)
    interp. Platform of the that media will share in
            id is the primary key that automaticly
               given and use as enumatation
             name is the partner's name
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RecordLabel(models.Model):
    """
    RecordLabel is RecordLabel(user=User, name=String)
    interp. RecordLabel is the label company for media
            user is the label company user (if any)
            name is the label name
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Track(models.Model):
    """
    Track is Track(media=FILE)
    interp. track is the media file
            media is the FILE
            otherArtists is OtherArtist for split paying
    """
    # number = models.IntegerField()
    name = models.CharField(max_length=150)
    media = models.FileField(upload_to='tracks')
    OtherArtists = models.ManyToManyField(OtherArtist,
                                          related_name='otherArtists_set',
                                          blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='subgenres',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Album(models.Model):
    """
    Album is Album(mediaType=mediaType, title=String, artist=Artist,
                   genre=String, subgenre=String,
                   recordLabel=String, releaseDate=Date,
                   platforms=Platform)
    interp. Album ia music or music video or any media
            mediaType is MediaType Choices
            tracks is Track list
            title is the media's title
            artwork is the album cover image
            artist is the media's Artist
            genre, subgenre is the media's genre
            partners is Partner
    """
    class statusType(models.IntegerChoices):
        PENDING = 0, _('Pending')
        INPROGRESS = 1, _('in Progress')
        CONFIRMED = 2, _('Confirmed')
        REJECTED = 3, _('Rejected')
        __empty__ = _('Please Select...')

    class mediaType(models.IntegerChoices):
        SINGLE = 0, _('Single')
        EP = 1, _('EP')
        ALBUM = 2, _('Album')
        __empty__ = _('Please Select...')

    mediaType = models.IntegerField(choices=mediaType.choices)
    tracks = models.ManyToManyField(Track,
                                    related_name='tracks_set')
    title = models.CharField(max_length=150)
    artwork = models.ImageField(upload_to='media/cover')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    artist_label = models.CharField(max_length=150, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    recordLabel = models.ForeignKey(RecordLabel, on_delete=models.CASCADE,
                                    null=True)
    releaseDate = models.DateField()
    platforms = models.ManyToManyField(Platform,
                                       related_name='platforms_set')
    status = models.IntegerField(choices=statusType.choices, default=0)

    def __str__(self):
        try:
            return self.title + ' by ' + self.artist.name
        except AttributeError:
            return (self.title +
                    ' by ' + self.artist_label + ' (' +
                    self.recordLabel.name + ')')


'''
-----------------------------
    Content ID Model
-----------------------------
         ContentID
-----------------------------
'''


class ContentID(models.Model):
    """
    ContentID is ContentID(title=String, url=URL, status=statusType Choices)
    interp. ContentID is Youtube removal request
             title is the Media's title
             url is media's URL
             status is statusType
    """
    class statusType(models.IntegerChoices):
        PENDING = 0, _('Pending')
        RECIEVED = 1, _('Removal Request Received')
        __empty__ = _('Please Select...')

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    status = models.IntegerField(choices=statusType.choices, default=0)

    def __str__(self):
        return self.title + ' by ' + self.user.username


'''
-----------------------
     Statistic Model
-----------------------
'''


class Statistic(models.Model):
    """
    Statistic is Statistic(track=Track, Platform, stream=Integer,
                           download=Integer, revenue=Integer)
     interp. Statistic is Track's statistic
             track is track with statistic
             platform is Platform
             stream is the stream count of media on that platform
             revenue is the money comes from platform
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    stream = models.IntegerField()
    download = models.IntegerField()
    revenue = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.album.title


'''
----------------------
     SplitStatement
----------------------
'''


class SplitStatement(models.Model):
    """SplitStatement is SplitStatement(track=Track, revenue=Integer,
                                        date=DateField)
    interp. SplitStatement is track's seperated revenue report
            track is Track
            revenue is Track's this month's revenue
            date is which month is revenue has come
    """
    class statusType(models.IntegerChoices):
        PENDING = 0, _('Pending')
        RECIEVED = 1, _('Statement Recieved')
        __empty__ = _('Please Select...')

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    revenue = models.IntegerField()
    date = models.DateField()
    status = models.IntegerField(choices=statusType.choices, default=0)

    def __str__(self):
        return self.track.name


'''
-----------------------
     Statement Model
-----------------------
'''


# Statement is Statement(album=Album, revenue=Integer, date=DateField)
# interp. Statement is Album's revenue report
#         album is Album
#         revenue is Album's this month's revenue
#         date is which month is renevue has come
class Statement(models.Model):
    '''Statement is Statement(album=Album, revenue=Integer, date=DateField)
     interp. Statement is Album's revenue report
             album is Album
             revenue is Album's this month's revenue
             date is which month is renevue has come
    '''
    class statusType(models.IntegerChoices):
        PENDING = 0, _('Pending')
        RECIEVED = 1, _('Statement Recieved')
        __empty__ = _('Please Select...')

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    revenue = models.IntegerField()
    date = models.DateField()
    splits = models.ManyToManyField(SplitStatement, related_name='split_set')
    status = models.IntegerField(choices=statusType.choices, default=0)

    def __str__(self):
        return self.album.title


'''
-----------------------
     Announcement Model
-----------------------
'''


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
