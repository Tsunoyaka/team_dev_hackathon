from rest_framework import serializers

from .models import Album, MusAlbum, AddAlbum


class AddAlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    add_album = serializers.StringRelatedField(source='album.album')
    image = serializers.StringRelatedField(source='album.image')
    add_slug = serializers.StringRelatedField(source='album.slug')
    album_creator = serializers.StringRelatedField(source='album.user')

    class Meta:
        model = AddAlbum
        fields = '__all__'

    def validate_album(self, album):
        user = self.context['request'].user
        slug = str(album).split('object')[1].strip(' ').strip('()')
        model = AddAlbum.objects.filter(user=user,album=album)
        model_album = Album.objects.filter(user=user, slug=slug)
        if model or model_album:
            raise serializers.ValidationError('У вас уже есть этот альбом!')
        return album

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    album_creator = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Album
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

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


class MusAlbumSerializer(serializers.ModelSerializer):
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
        album = self.context['request'].data['album']
        model = MusAlbum.objects.filter(musics=musics, album=album)
        if model:
            raise serializers.ValidationError('Эта музыка уже есть в альбоме!')
        return super().validate(musics)

    class Meta:
        model = MusAlbum
        fields = '__all__'

