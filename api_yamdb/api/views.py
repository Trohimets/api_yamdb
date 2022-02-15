from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404


from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import IsAdmin, AuthUserOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          ReviewSerializer, CommentSerializer, TokenSerializer,
                          SignupSerializer, UserSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import User
from reviews.models import Category, Genre, Title, Review


SUBJECT = 'YaMDb: код подверждения'
MESSAGE = 'Ваш код подтверждения - {}'
FIELD_ERROR = 'Неуникальное поле. Ошибка - {}'


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('username')
    try:
        user, created = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
    except IntegrityError as error:
        raise ValidationError(FIELD_ERROR.format(error))
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        SUBJECT,
        MESSAGE.format(confirmation_code),
        DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )
    if not default_token_generator.check_token(
            user,
            serializer.data['confirmation_code']):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    data = {
        'token': str(token),
    }
    return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    ordering_fields = ('year', 'name')
    permission_classes = [IsAdmin | ReadOnly]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitlePostSerializer


class RecordViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthUserOrReadOnly,)
    base_model = None
    id_name = None
    record_name = None

    def get_base_record(self):
        record = get_object_or_404(
            self.base_model, pk=self.kwargs.get(self.id_name)
        )
        return record

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            **{self.record_name: get_object_or_404(
                self.base_model, pk=self.kwargs.get(self.id_name)
            )
            }
        )


class ReviewViewSet(RecordViewSet):
    serializer_class = ReviewSerializer
    base_model = Title
    id_name = "title_id"
    record_name = "title"

    def get_queryset(self):
        return self.get_base_record().reviews.all()


class CommentViewSet(RecordViewSet):
    serializer_class = CommentSerializer
    base_model = Review
    id_name = "review_id"
    record_name = "review"

    def get_queryset(self):
        return self.get_base_record().comments.all()
