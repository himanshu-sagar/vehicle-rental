from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )  # only used for password validation

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'password',
            'confirm_password',
            'is_admin',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Check that the two password fields match
        if data['password'] != data['confirm_password']:
            raise ValidationError("The two password fields didn't match.")
        return data

    def create(self, validated_data):
        del validated_data["confirm_password"]
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Set password for the user after encoding it with hash function
        user.save()
        return user