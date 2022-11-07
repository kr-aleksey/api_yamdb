from django.urls import path, include
from rest_framework import routers

from .views import (
    SignupView,
    UserViewSet,
    TokenObtainView,
    MeUserView,
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
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

    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('v1/users/me/', MeUserView.as_view(), name='me_user'),
    path('v1/', include(v1_router.urls)),
]
