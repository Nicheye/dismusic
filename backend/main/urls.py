from django.urls import path, include
from rest_framework.routers import SimpleRouter
from main.views import AlbumViewSet, LikeDislikeView, TrackView, PlayView
from main.views import FavPlaylistView, DisPlaylistView

router = SimpleRouter()
router.register(r'albums', AlbumViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('react/', LikeDislikeView.as_view()),
    path('react/<int:id>/', LikeDislikeView.as_view()),
    path('tracks/<int:id>/', TrackView.as_view()),
    path('play/<int:id>/', PlayView.as_view()),
    path('favorites/', FavPlaylistView.as_view()),
    path('disliked/', DisPlaylistView.as_view()),

]
