# Generated by Django 3.0.2 on 2020-01-21 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_otherartist_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.IntegerField()),
                ('date', models.DateField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Album')),
            ],
        ),
    ]
