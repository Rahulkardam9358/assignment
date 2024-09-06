from rest_framework import generics, status, response
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.serializers import UserSerializer, UserCreateSerializer, \
    FriendRequestSentSerializer, FriendRequestReceiveSerializer, \
    SendFriendRequestSerializer, AcceptFriendRequestSerializer
from authentication.models import User, FriendRequest
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UserRegisterUser(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny, ]


class GetUserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.query_params.get('search', '')
        if not search_keyword:
            return queryset

        if '@' in search_keyword:
            return queryset.filter(email__iexact=search_keyword)
        return queryset.filter(
            Q(first_name__icontains=search_keyword) | Q(last_name__icontains=search_keyword)
        )


class SentRequestsView(generics.ListAPIView):
    '''List all friend requests that are sent from user'''
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user, status='pending')


class ReceiveRequestsView(generics.ListAPIView):
    '''List all pending friend requests'''
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestReceiveSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user, status='pending')


class FriendsListView(generics.ListAPIView):
    '''List all friends'''
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        friend_ids = FriendRequest.objects.filter(
            sender=self.request.user, 
            status='accepted'
        ).values_list(
            'receiver__id',
            flat=True
        )
        return self.queryset.filter(id__in=friend_ids)


class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            receiver = serializer.validated_data['receiver']
            sender = request.user

            if sender == receiver:
                return response.Response({
                    'detail': 'You cannot send a friend request to yourself.'
                }, status=status.HTTP_400_BAD_REQUEST)

            now = timezone.now()
            time_limit = now - timezone.timedelta(minutes=1)
            recent_requests = FriendRequest.objects.filter(
                sender=sender,
                created_at__gte=time_limit
            ).count()

            if recent_requests >= 3:
                return response.Response({
                    'detail': 'Rate limit exceeded. You can only send 3 requests every 1 minutes.'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
                return response.Response({
                    'detail': 'Friend request already sent.'
                }, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest(sender=sender, receiver=receiver)
            friend_request.save()

            return response.Response({
                'detail': 'Friend request sent.'
            }, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(generics.CreateAPIView):
    serializer_class = AcceptFriendRequestSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            frndrqst = FriendRequest.objects.filter(sender=sender, receiver=request.user, status='pending')

            if not frndrqst.exists():
                return response.Response({
                    'detail': 'No friend request found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            frnd_request_obj = frndrqst.last()
            print("Friend Request Accept", frnd_request_obj, frnd_request_obj.status)

            frnd_request_obj.status = 'accepted'
            frnd_request_obj.save()

            return response.Response({
                'detail': 'Friend request accepted.'
            }, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(generics.CreateAPIView):
    serializer_class = AcceptFriendRequestSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            frndrqst = FriendRequest.objects.filter(sender=sender, receiver=request.user, status='pending')

            if not frndrqst.exists():
                return response.Response({
                    'detail': 'No friend request found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            frnd_request_obj = frndrqst.last()

            frnd_request_obj.status = 'rejected'
            frnd_request_obj.save()

            return response.Response({
                'detail': 'Friend request rejected.'
            }, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)