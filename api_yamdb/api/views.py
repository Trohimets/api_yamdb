from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .permissions import IsRoleAdmin
from .serializers import TokenSerializer, SignupSerializer, UserSerializer
from api_yamdb.settings import DEFAULT_FROM_EMAIL

SUBJECT = 'YaMDb: код подверждения'
MESSAGE = 'Ваш код подтверждения - {}'
USERNAME_ERROR = 'Имя пользователя не может быть "me"'
FIELD_ERROR = 'Неуникальное поле. Ошибка - {}'

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('username')
    if user == 'me':
        raise ValidationError(USERNAME_ERROR)
    try:
        user, created = User.objects.get_or_create(
            email=serializer.data['email'],
            username=serializer.data['username'],
        )
    except IntegrityError as error:
            raise ValidationError(FIELD_ERROR.format(error))
    if created:
        user.save()
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
        username=serializer.data['username'],
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
    lookup_field = 'username'
    permission_classes = [IsRoleAdmin]

    def perform_create(self, serializer):
        serializer.save()

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
