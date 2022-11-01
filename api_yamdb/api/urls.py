from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
:
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', TokenObtainPairView.as_view(), name='signup'),
]