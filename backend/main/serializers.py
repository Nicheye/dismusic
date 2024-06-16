from rest_framework import serializers
from main.models import Album, Track, Like, DisLike


class AlbumSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['title', 'created_by', 'created_at', 'cover', 'tracks',
                  'url']

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_cover(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_tracks(self, obj):
        tracks_query = Track.objects.filter(album=obj)
        tracks_ser = TrackSerializer(tracks_query, many=True,
                                     context=self.context)
        return tracks_ser.data

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'{obj.id}')
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d %B')


class TrackSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    rec = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ['title', 'likes', 'dislikes', 'is_liked',
                  'is_disliked',
                  'streams',
                  'rec']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated is True:
            like_obj = Like.objects.get(liked_by=user, track=obj)

            if like_obj:
                self.is_disliked = False
                return True
            else:
                return False
        return False

    def get_is_disliked(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if user.is_authenticated is True:

            dislike_obj = DisLike.objects.get(disliked_by=user, track=obj)

            if dislike_obj:
                return True
            else:
                return False
        return False

    def get_rec(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(obj.rec.url)
        return None
