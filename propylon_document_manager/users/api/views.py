import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from propylon_document_manager.users.api.serializers import UserSerializer, RegisterSerializer

from propylon_document_manager.utils.utils import validate_register_fields

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = self.serializer_class(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterView(APIView):
    authentication_classes = []  # Exclude authentication for this view
    permission_classes = []  # Allow any user, authenticated or not
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        logging.info('RegisterView -> request.data: {}'.format(request.data))
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')
        logging.info('username={},password={},email={}'.format(username,password,email))
        error_infos = validate_register_fields(username=username, email=email, password=password)
        if error_infos!='':
            return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={error_infos})
        if len(User.objects.filter(email=email)) != 0:
            return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={'email already exist!'})
        data['password'] = make_password(password)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data='Register successful!')
        return Response(status=status.HTTP_205_RESET_CONTENT, data=serializer.errors)


class LoginView(ObtainAuthToken):
    # serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        # username: "stone@gmail.com" -->email , password:"yezhenxu"
        logging.info('LoginView22 -> request.data: {}'.format(request.data))
        data = request.data
        password = data.get('password', '')
        email = data.get('username', '')
        logging.info('password={},email={}'.format(password, email))
        user_query = User.objects.filter(email = email)
        if not user_query.exists():
            return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={'email no exist!'})
        user_infos = user_query.values('password','id')[0]
        if not check_password(password, user_infos['password']):
            return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={'password is wrong!'})
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(status=status.HTTP_200_OK, data={'token': token.key, 'user_id': user.pk})
        return Response(status=status.HTTP_206_PARTIAL_CONTENT,data=serializer.errors)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Delete the token associated with the user
        logging.info('LogoutView ->request.data= {}'.format(request.data))
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK, data='Logout successful!')
