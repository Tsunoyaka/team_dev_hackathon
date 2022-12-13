from rest_framework import serializers

from .models import Music, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField(source='artist.username')

    class Meta:
        model = Music
        fields = '__all__'

class MusicCreateSerializer(serializers.ModelSerializer):
    artist = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='artist.username'
    )

    class Meta:
        model = Music
        fields = '__all__'


    def validate(self, attrs):
        artist = self.context['request'].user
        attrs['artist'] = artist
        return attrs


    