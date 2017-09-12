from django.contrib.auth.models import User
from drf_role.models import Role
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models.profile import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'is_active')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('pk', 'name', 'type')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('pk', 'user', 'role', 'date_of_birth', 'gender', 'mobile', 'address')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'password')


class RegistrationSerializer(serializers.Serializer):
    role = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        user = User.objects.filter(username=username).first()
        if user:
            raise ValidationError({"username": ["username already exists."]})

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError({"non_fields_errors": ["password and confirm_password do not match."]})

        # Remove confirm password from attrs
        attrs.pop('confirm_password')
        return attrs

    class Meta:
        fields = ('role', 'username', 'password', 'confirm_password', 'email', 'gender')
