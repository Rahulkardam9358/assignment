from django.urls import path
from authentication.views import GetUserDetailView, UserRegisterUser, UserListView, \
    SentRequestsView, ReceiveRequestsView, SendFriendRequestView, AcceptFriendRequestView, \
    FriendsListView, RejectFriendRequestView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('auth/create-user/', UserRegisterUser.as_view()),
    path('auth/create-token/', TokenObtainPairView.as_view()),
    path('auth/create-access/', TokenRefreshView.as_view()),
    path('auth/verify-access/', TokenVerifyView.as_view()),
    path('auth/me/', GetUserDetailView.as_view()),
    path('auth/list-user/', UserListView.as_view()),
    path('auth/list-friends/', FriendsListView.as_view()),
    path('auth/list-sent-requests/', SentRequestsView.as_view()),
    path('auth/list-receive-requests/', ReceiveRequestsView.as_view()),
    path('auth/send-request/', SendFriendRequestView.as_view()),
    path('auth/accept-request/', AcceptFriendRequestView.as_view()),
    path('auth/reject-request/', RejectFriendRequestView.as_view()),
]