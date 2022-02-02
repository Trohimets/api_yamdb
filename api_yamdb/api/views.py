from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Category
from reviews.models import Genre
from reviews.models import Title
from .serializers import CategorySerializer
from .serializers import GenreSerializer
from .serializers import TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
