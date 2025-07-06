from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='userprofile')
router.register(r'workspaces', views.WorkspaceViewSet, basename='workspace')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
