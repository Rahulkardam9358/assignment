from rest_framework import serializers
from authentication.models import User, FriendRequest


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }


class FriendRequestSentSerializer(serializers.ModelSerializer):
    receiver = UserCreateSerializer(many=False)
    class Meta:
        model = FriendRequest
        fields = ['receiver', 'created_at',]
        extra_kwargs = {
            'created_at': {
                'read_only': True
            }
        }


class FriendRequestReceiveSerializer(serializers.ModelSerializer):
    sender = UserCreateSerializer(many=False)
    class Meta:
        model = FriendRequest
        fields = ['sender', 'created_at',]
        extra_kwargs = {
            'created_at': {
                'read_only': True
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class SendFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['receiver']


class AcceptFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender']