from rest_framework import serializers
from reviews.models import Title, Genre, Category, Review, Comment
from django.shortcuts import get_object_or_404

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'id', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = GenreSerializer(many=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'category',
                  'genre', 'year')

    def create(self, validated_data):
        # Уберем список достижений из словаря validated_data и сохраним его
        genre = validated_data.pop('genre')

        # Создадим нового котика пока без достижений, данных нам достаточно
        title = Title.objects.create(**validated_data, genre=genre)
        return title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'id', 'slug')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'pub_date', 'score')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'review', 'text', 'pub_date')
