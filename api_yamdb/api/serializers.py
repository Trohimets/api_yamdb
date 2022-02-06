import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import serializers
from reviews.models import Title, Genre, Category, Review, Comment
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        max_length=100,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


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

    def validate_year(self, value):
        year = dt.date.today().year
        if value>year:
            raise serializers.ValidationError('Год не может быть больше текущего!')
        return value

      
class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

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
