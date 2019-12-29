from django.db import models
from django.utils.translation import gettext as _


# Artist is Artist(name=String)
# interp. Main Artist of the media
#         name is the main artist name of media       String
class Artist(models.Model):
    name = models.CharField(max_length=100)

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


# Partner is Partner(name=String)
# interp. Partner of the that media will share in
#         id is the primary key that automaticly
#            given and use as enumatation
#         name is the partner's name                 String
class Partner(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Track is Track(media=FILE)
# interp. track is the media file
#         media is the FILE
class Track(models.Model):
    media = models.FileField()


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
#         appleArtist, spotifyArtist is the URL
#         partners is Partner
#         otherArtists is OtherArtist for split paying
class Album(models.Model):

    class MediaType(models.IntegerChoices):
        SINGLE = 0, _('Single')
        EP = 1, _('EP')
        ALBUM = 2, _('Album')
        __empty__ = _('Please Select...')

    mediaType = models.IntegerField(choices=MediaType.choices)
    tracks = models.ManyToManyField(Track,
                                    related_name='tracks_set')
    title = models.CharField(max_length=150)
    artwork = models.ImageField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    subgenre = models.CharField(max_length=50, null=True)
    appleArtist = models.URLField(null=True)
    spotifyArtist = models.URLField(null=True)
    recordLabel = models.CharField(max_length=150)
    releaseDate = models.DateField()
    partners = models.ManyToManyField(Partner,
                                      related_name='partners_set')
    OtherArtists = models.ManyToManyField(OtherArtist,
                                          related_name='otherArtists_set')

    def __str__(self):
        return self.title + ' by ' + self.artist.name
