from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    ReviewViewSet,
    CommentViewSet
)

v1_router = routers.DefaultRouter()
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'title/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', TokenObtainPairView.as_view(), name='signup'),
]
