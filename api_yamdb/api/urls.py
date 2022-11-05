from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    SignupView,
    UserViewSet,
    TokenObtainView,
    ReviewViewSet,
    CommentViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register(
    r'users',
    UserViewSet,
    basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('v1/auth/token2/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
