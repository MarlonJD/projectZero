from rest_framework import serializers
from panel.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'parent', 'name']
