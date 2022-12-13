from rest_framework import serializers

from .models import Album, MusAlbum

class AlbumSerializer(serializers.ModelSerializer):
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
                'musics': 'http://127.0.0.1:8000/media/' + i['musics']
                }
                music_list.append(obj)
        representation['musics'] = music_list
        return representation

class MusAlbumSerializer(serializers.ModelSerializer):
    musics = serializers.StringRelatedField(source='musics.music')

    class Meta:
        model = MusAlbum
        fields = ['id', 'musics']

