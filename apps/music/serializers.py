from rest_framework import serializers

from .models import Music, Genre, LikeMusic


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

class CurrentMusicDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['music'] 


class LikeSerializer(serializers.ModelSerializer):
    image = serializers.StringRelatedField(source='like_music.image')
    music = serializers.StringRelatedField(source='like_music.music')

    class Meta:
        model = LikeMusic
        fields = '__all__'


class LikeMusicSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )
    like_music = serializers.HiddenField(default=CurrentMusicDefault())

    class Meta:
        model = LikeMusic
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        like_music = self.context.get('music').pk
        like = LikeMusic.objects.filter(user=user, like_music=like_music).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        like_music = self.context.get('music').pk
        like = LikeMusic.objects.filter(user=user, like_music=like_music).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')
