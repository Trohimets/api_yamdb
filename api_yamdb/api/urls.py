from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import signup, token, UserViewSet
from api.views import TitleViewSet, GenreViewSet
from api.views import CategoryViewSet, ReviewViewSet, CommentViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)',
    TitleViewSet,
    basename='title_detail')
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'genres/(?P<slug>[-\w]+)',
    GenreViewSet,
    basename='genre_delete')
router_v1.register('categories', CategoryViewSet, basename='categories')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),  
]
