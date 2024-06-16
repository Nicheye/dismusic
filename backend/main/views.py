from  rest_framework import viewsets
from rest_framework.response import Response
from main.models import Album,Track,Like,DisLike
from main.serializers import AlbumSerializer,TrackSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

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

class Like_Dislike_View(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id",None)
        user = request.user

        if id is None:
            return Response({'message':'you havent provided any id'},status = status.HTTP_400_BAD_REQUEST)
        
        track_obj = Track.objects.get(id=id)

        if track_obj:
            like = Like.objects.get(track=track_obj,liked_by=user)

            if like:
                return Response({'message':'you have liked this post'},status = status.HTTP_200_OK)
            
            dislike = DisLike.objects.get(track=track_obj,liked_by=user)

            if dislike:
                return Response({'message':'you have disliked this post'},status = status.HTTP_200_OK)
            
            return Response({'message':'you havent reacted to this post'}, status= status.HTTP_204_NO_CONTENT)
        
        return Response({'message':'no track obj'}, status= status.HTTP_204_NO_CONTENT)

    ###for like
    def patch(self,request,*args,**kwargs):
        track_id = kwargs.get('id',None)
        user = request.user

        if track_id is None:
            return Response({'message':'you havent provided any id for a track'})
        
        track_obj = Track.objects.get(id=track_id)
        
        if track_obj:
            like_check = Like.objects.get(track=track_obj,liked_by=user)

            if like_check:
                like_check.delete()
                track_obj.likes -= 1
                track_obj.save()
                return Response(
                    {'message':'you have already liked this post, but we guess you wanted to put off your like'},
                    status = status.HTTP_208_ALREADY_REPORTED
                    )
            
            dislike_check = DisLike.objects.get(track=track_obj,disliked_by=user)

            if dislike_check:
                dislike_check.delete()
                track_obj.dislikes -= 1
                track_obj.save()
                return Response(
                    {'message':'you have already disliked this post, but we guess you wanted to put off your dislike'},
                    status = status.HTTP_208_ALREADY_REPORTED
                    )
            
            like_obj = Like.objects.create(track=track_obj,liked_by=user)
            track_obj.likes+=1
            track_obj.save()
            return Response({'message':'gratz! you liked your post'}, status=status.HTTP_201_CREATED)
        
        return Response({'message':'no track obj'}, status=status.HTTP_400_BAD_REQUEST)
    
    ###for dislike
    def put(self,request,*args,**kwargs):
        track_id = kwargs.get('id',None)
        user = request.user

        if track_id is None:
            return Response({'message':'you havent provided any id for a track'})
        
        track_obj = Track.objects.get(id=track_id)
        
        if track_obj:
            like_check = Like.objects.get(track=track_obj,liked_by=user)

            if like_check:
                like_check.delete()
                track_obj.likes -= 1
                track_obj.save()
                return Response(
                    {'message':'you have already liked this post, but we guess you wanted to put off your like'},
                    status = status.HTTP_208_ALREADY_REPORTED
                    )
            
            dislike_check = DisLike.objects.get(track=track_obj,disliked_by=user)

            if dislike_check:
                dislike_check.delete()
                track_obj.dislikes -= 1
                track_obj.save()
                return Response(
                    {'message':'you have already disliked this post, but we guess you wanted to put off your dislike'},
                    status = status.HTTP_208_ALREADY_REPORTED
                    )
            
            dislike_obj = DisLike.objects.create(track=track_obj,liked_by=user)
            track_obj.likes+=1
            track_obj.save()
            return Response({'message':f'gratz! you disliked your post {dislike_obj.id}'}, status=status.HTTP_201_CREATED)
        
        return Response({'message':'no track obj'}, status=status.HTTP_400_BAD_REQUEST)


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

            






