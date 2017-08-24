from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.profile import Profile
from core.serializers.profile_serializers import *


class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter()


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            try:
                profile = Profile.objects.get(pk=user.pk)
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                response = {
                    "token": token.key,
                    "user_role": profile.role.name
                }
                return Response(response)
            except (Profile.DoesNotExist, AttributeError):
                error_response = {"non_fields_error": ["Authentication credentials may be wrong. Please try again."]}
                return Response(error_response)


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_reg_serializer = RegistrationSerializer(data=request.data)
        if user_reg_serializer.is_valid(raise_exception=True):
            pass
