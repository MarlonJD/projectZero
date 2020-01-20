# Generated by Django 3.0.1 on 2020-01-20 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mediaType', models.IntegerField(choices=[(None, 'Please Select...'), (0, 'Single'), (1, 'EP'), (2, 'Album')])),
                ('title', models.CharField(max_length=150)),
                ('artwork', models.ImageField(upload_to='')),
                ('genre', models.CharField(max_length=50)),
                ('subgenre', models.CharField(max_length=50, null=True)),
                ('recordLabel', models.CharField(max_length=150)),
                ('releaseDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('appleArtist', models.URLField(null=True)),
                ('spotifyArtist', models.URLField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtherArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                ('media', models.FileField(upload_to='media')),
                ('OtherArtists', models.ManyToManyField(related_name='otherArtists_set', to='panel.OtherArtist')),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream', models.IntegerField()),
                ('download', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('date', models.DateField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Album')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Platform')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Track')),
            ],
        ),
        migrations.CreateModel(
            name='RecordLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContentID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('status', models.IntegerField(choices=[(None, 'Please Select...'), (0, 'Pending'), (1, 'Removal Request Received')], default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='platforms',
            field=models.ManyToManyField(related_name='partners_set', to='panel.Platform'),
        ),
        migrations.AddField(
            model_name='album',
            name='tracks',
            field=models.ManyToManyField(related_name='tracks_set', to='panel.Track'),
        ),
    ]