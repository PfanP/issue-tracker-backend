from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_role.enums import RoleEnum
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.profile import Profile
from core.serializers.profile_serializers import ProfileSerializer, LoginSerializer, RegistrationSerializer


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
                token, _created = Token.objects.get_or_create(user_id=user.pk)
                response = {
                    "token": token.key,
                    "user_role": profile.role.name
                }
                return Response(response)
            except (Profile.DoesNotExist, AttributeError):
                error_response = {"non_fields_error": ["Authentication credentials may be wrong. Please try again."]}
                return Response(error_response)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response_data = {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Successfully logout."
        }
        try:
            request.user.auth_token.delete()
            return Response(data=response_data)
        except (AttributeError, ObjectDoesNotExist):
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['message'] = "Failed to logout. Please contact."
            return Response(data=response_data)


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            role = serializer.validated_data.get('role', RoleEnum.STAFF.value)
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            gender = serializer.validated_data.get('gender')

            # Create user first
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                profile = Profile.objects.create(
                    user_id=user.pk,
                    role_id=role,
                    gender=gender
                )
                if profile:
                    data = serializer.validated_data
                    data['message'] = "An verification link has sent to {0}.".format(data.get('email'))
                    data.pop('password')  # Trick to remove password from response
                    return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
