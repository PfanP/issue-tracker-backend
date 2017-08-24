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
        fields = ('user', 'role', 'date_of_birth', 'gender', 'mobile', 'address')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'password')


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if not username:
            raise ValidationError({"username": ["This field is required."]})
        if not password:
            raise ValidationError({"password": ["This field is required."]})
        if not confirm_password:
            raise ValidationError({"confirm_password": ["This field is required."]})

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError({"non_fields_errors": ["password and confirm_password do not match."]})
        return attrs

    class Meta:
        fields = ('username', 'password', 'confirm_password')
