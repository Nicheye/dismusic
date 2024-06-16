from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from main.models import Album, Track, Like, DisLike
from main.serializers import AlbumSerializer, TrackSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.order_by('created_at').all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context

    def create(self, request):
        data = request.data
        user = request.user
        serializer = AlbumSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            cover = request.FILES.get('cover')
            serializer.save(created_by=user, cover=cover)
            return Response({'data': serializer.data},
                            status=status.HTTP_201_CREATED)


class LikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        track_id = kwargs.get('id', None)
        user = request.user

        if track_id is None:
            return Response({'message': 'You haven\'t provided any id'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            track_obj = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'message': 'No track object'},
                            status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(track=track_obj, liked_by=user).first()
        if like:
            return Response({'message': 'You have liked this post'},
                            status=status.HTTP_200_OK)

        dislike = DisLike.objects.filter(track=track_obj, disliked_by=user).first()
        if dislike:
            return Response({'message': 'You have disliked this post'},
                            status=status.HTTP_200_OK)

        return Response({'message': 'You haven\'t reacted to this post'},
                        status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        track_id = kwargs.get('id', None)
        user = request.user

        if track_id is None:
            return Response({'message': 'You haven\'t provided any id for a track'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            track_obj = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'message': 'No track object'},
                            status=status.HTTP_404_NOT_FOUND)

        like_check = Like.objects.filter(track=track_obj, liked_by=user).first()
        if like_check:
            like_check.delete()
            track_obj.likes -= 1
            track_obj.save()
            return Response(
                {'message': 'You have already liked this post, but we guess you wanted to remove your like'},
                status=status.HTTP_208_ALREADY_REPORTED
            )

        dislike_check = DisLike.objects.filter(track=track_obj, disliked_by=user).first()
        if dislike_check:
            dislike_check.delete()
            track_obj.dislikes -= 1
            track_obj.save()
            return Response(
                {'message': 'You have already disliked this post, but we guess you wanted to remove your dislike'},
                status=status.HTTP_208_ALREADY_REPORTED
            )

        Like.objects.create(track=track_obj, liked_by=user)
        track_obj.likes += 1
        track_obj.save()
        return Response({'message': 'You liked the post'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        track_id = kwargs.get('id', None)
        user = request.user

        if track_id is None:
            return Response({'message': 'You haven\'t provided any id for a track'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            track_obj = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({'message': 'No track object'},
                            status=status.HTTP_404_NOT_FOUND)

        like_check = Like.objects.filter(track=track_obj, liked_by=user).first()
        if like_check:
            like_check.delete()
            track_obj.likes -= 1
            track_obj.save()
            return Response(
                {'message': 'You have already liked this post, but we guess you wanted to remove your like'},
                status=status.HTTP_208_ALREADY_REPORTED
            )

        dislike_check = DisLike.objects.filter(track=track_obj, disliked_by=user).first()
        if dislike_check:
            dislike_check.delete()
            track_obj.dislikes -= 1
            track_obj.save()
            return Response(
                {'message': 'You have already disliked this post, but we guess you wanted to remove your dislike'},
                status=status.HTTP_208_ALREADY_REPORTED
            )

        DisLike.objects.create(track=track_obj, disliked_by=user)
        track_obj.dislikes += 1
        track_obj.save()
        return Response({'message': f'You disliked the post {track_obj.id}'}, status=status.HTTP_201_CREATED)


class TrackView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if id is None:
            queryset = Track.objects.all()
            serializer = TrackSerializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        track_obj = Track.objects.get(id=id)
        if track_obj is None:
            return Response({'message': 'no such track'}, status=status.HTTP_404_NOT_FOUND)
        track_ser = TrackSerializer(track_obj)
        return Response({'data': track_ser.data}, status=status.HTTP_302_FOUND)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        id = kwargs.get('id', None)
        if id is None:
            return Response({'message': 'you havent provided any id'}, status=status.HTTP_400_BAD_REQUEST)
        album_obj = Album.objects.get(id=id)
        if album_obj is None or album_obj.created_by != user:
            return Response({'message': 'no such album'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TrackSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            rec = request.FILES.get('rec')
            serializer.save(album=album_obj, created_by=user, rec=rec)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        id = kwargs.get('id', None)
        if id is None:
            return Response({'message': 'you havent provided any id'}, status=status.HTTP_400_BAD_REQUEST)
        track_instance = Track.objects.get(id=id)
        if track_instance is None or track_instance.created_by != user:
            return Response({'message': 'no such album'}, status=status.HTTP_400_BAD_REQUEST)
        track_ser = TrackSerializer(track_instance, data=data)
        if track_ser.is_valid(raise_exception=True):
            track_ser.save()
            return Response({'data': track_ser.data}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get('id', None)
        if id is None:
            return Response({'message': 'you havent provided any id'}, status=status.HTTP_400_BAD_REQUEST)
        track_instance = Track.objects.get(id=id)
        if track_instance is None or track_instance.created_by != user:
            return Response({'message': 'no such album'}, status=status.HTTP_400_BAD_REQUEST)
        track_instance.delete()
        return Response({'message': 'track deleted'}, status=status.HTTP_410_GONE)


class PlayView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if id is None:
            return Response({'message': 'you havent provided any id'}, status=status.HTTP_400_BAD_REQUEST)
        track_obj = Track.objects.get(id=id)
        if track_obj is None:
            return Response({'message': 'no such album'}, status=status.HTTP_400_BAD_REQUEST)
        track_obj.streams += 1
        track_obj.save()
        track_ser = TrackSerializer(track_obj, context={'request': request})
        return Response({'data': track_ser.data}, status=status.HTTP_200_OK)


class FavPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_tracks = Track.objects.filter(like__liked_by=user)
        tracks_ser = TrackSerializer(liked_tracks, many=True)
        return Response({'data': tracks_ser.data}, status=status.HTTP_200_OK)


class DisPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_tracks = Track.objects.filter(dislike__disliked_by=user)
        tracks_ser = TrackSerializer(liked_tracks, many=True)
        return Response({'data': tracks_ser.data}, status=status.HTTP_200_OK)
