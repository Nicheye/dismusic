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


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
        })
        return context