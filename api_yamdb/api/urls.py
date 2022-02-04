from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet, GenreViewSet
from api.views import CategoryViewSet, ReviewViewSet, CommentViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)',
    TitleViewSet,
    basename='title_detail')
router.register('genres', GenreViewSet)
router.register(
    r'genres/(?P<slug>[-\w]+)',
    GenreViewSet,
    basename='genre_delete')
router.register('categories', CategoryViewSet, basename='categories')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]


router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'posts/(?P<post_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet, basename='comment_detail'
)