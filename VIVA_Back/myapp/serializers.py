from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # Confirm Password

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The two passwords you entered do not match！")
        return data

    def create(self, validated_data):
        validated_data.pop('password2') # Delete confirmation password
        return User.objects.create(**validated_data)
