from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, TokenObtainView, SignupView

v1_router = routers.DefaultRouter()
v1_router.register(
    r'users',
    UserViewSet,
    basename='user')

urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('v1/', include(v1_router.urls)),
]
