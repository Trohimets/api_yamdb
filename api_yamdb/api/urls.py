from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet, GenreViewSet
from api.views import CategoryViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
