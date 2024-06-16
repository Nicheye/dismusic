from django.urls import path, include
from rest_framework.routers import SimpleRouter
from main.views import AlbumViewSet, TrackViewSet, LikeDislikeView

router = SimpleRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('react/', LikeDislikeView.as_view()),
    path('react/<int:id>/', LikeDislikeView.as_view()),

]
