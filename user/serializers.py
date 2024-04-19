from django.shortcuts import redirect
from rest_framework import serializers
from django.contrib.auth import get_user_model, logout
from rest_framework.validators import UniqueValidator
User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=100)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")]
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'password', 'confirm_password']

    def validate(self, attrs):
        username = attrs['first_name'] + ' ' + attrs['last_name']
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise serializers.ValidationError({'error': 'Username already exists'})
        attrs['username'] = username

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Password and Confirm Password are not matching.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data, is_active=False)
        return user


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100, label="Username Or Email")
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Registered Email ID", required=True)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, label="Password")
    confirm_password = serializers.CharField(label="Confirm Password", required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Password and Confirm Password are Matching.'})
        return attrs