from rest_framework import serializers

from .models import Album, MusAlbum, AddAlbum


class AddAlbumSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField(source='album.album')
    image = serializers.StringRelatedField(source='album.image')
    slug = serializers.StringRelatedField(source='album.slug')
    album_creator = serializers.StringRelatedField(source='album.user')
    # image = serializers.StringRelatedField(source='musics.image')
    # time_length = serializers.StringRelatedField(source='musics.time_length')
    # genre = serializers.StringRelatedField(source='musics.genre')

    class Meta:
        model = AddAlbum
        fields = '__all__'



class AlbumSerializer(serializers.ModelSerializer):
    album_creator = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Album
        fields = '__all__'

class AlbumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        music = MusAlbumSerializer(instance.album_music.all(), many=True).data
        music_list = []
        if music:
            for i in music:
                obj = {
                'id': i['id'],
                'musics': 'http://127.0.0.1:8000/media/' + i['musics'],
                'title': i['title'],
                'artist': i['artist'],
                'image': 'http://127.0.0.1:8000/media/' + i['image'],
                'genre': i['genre'],
                'time_length': i['time_length']
                }
                music_list.append(obj)
        representation['musics'] = music_list
        return representation

class MusAlbumSerializer(serializers.ModelSerializer):
    musics = serializers.StringRelatedField(source='musics.music')
    title = serializers.StringRelatedField(source='musics.title')
    artist = serializers.StringRelatedField(source='musics.artist')
    image = serializers.StringRelatedField(source='musics.image')
    time_length = serializers.StringRelatedField(source='musics.time_length')
    genre = serializers.StringRelatedField(source='musics.genre')

    class Meta:
        model = MusAlbum
        fields = '__all__'

