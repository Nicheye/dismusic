from django.urls import path, include
from rest_framework.routers import SimpleRouter
from main.views import AlbumViewSet,TrackViewSet,Like_Dislike_View

router = SimpleRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('react/',Like_Dislike_View.as_view()),
    path('react/<int:id>/',Like_Dislike_View.as_view()),

]
