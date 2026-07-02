from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Bounty

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class BountySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bounty
        fields = ['id', 'target_name', 'reward', 'status', 'owner']

    def validate_status(self, value):
        if value not in ['wanted', 'captured']:
            raise serializers.ValidationError("Status must be exactly 'wanted' or 'captured'.")
        return value

    def validate_reward(self, value):
        if value < 0:
            raise serializers.ValidationError("The reward cannot be negative.")
        return value
