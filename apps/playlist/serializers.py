from rest_framework import serializers

from .models import Playlist, MusPlaylist


class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = Playlist
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs



class PlaylistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        music = MusPlaylistSerializer(instance.playlist_music.all(), many=True).data
        music_list = []
        if music:
            for i in music:
                obj = {
                'id': i['id'],
                'music': '/media/' + i['music'],
                'title': i['title'],
                'artist': i['user'],
                'image': '/media/' + i['image'],
                'genre': i['genre'],
                'time_length': i['time_length']
                }
                music_list.append(obj)
        representation['musics'] = music_list
        return representation


class MusPlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    music = serializers.StringRelatedField(source='musics.music')
    title = serializers.StringRelatedField(source='musics.title')
    user = serializers.StringRelatedField(source='musics.user')
    image = serializers.StringRelatedField(source='musics.image')
    time_length = serializers.StringRelatedField(source='musics.time_length')
    genre = serializers.StringRelatedField(source='musics.genre')

    def validate_musics(self, musics):
        playlist = self.context['request'].data['playlist']
        model = MusPlaylist.objects.filter(musics=musics, playlist=playlist)
        if model:
            raise serializers.ValidationError('Эта музыка уже есть в плейлисте!')
        return super().validate(musics)

    class Meta:
        model = MusPlaylist
        fields = '__all__'

