# Generated by Django 3.0.2 on 2020-01-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_auto_20200123_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='platforms',
            field=models.ManyToManyField(related_name='platforms_set', to='panel.Platform'),
        ),
    ]