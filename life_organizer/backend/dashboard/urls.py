from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'widgets', views.DashboardWidgetViewSet, basename='dashboardwidget')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'activities', views.UserActivityViewSet, basename='useractivity')

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', views.DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('preferences/', views.DashboardPreferencesView.as_view(), name='dashboard-preferences'),
    path('quick-stats/', views.QuickStatsView.as_view(), name='quick-stats'),
]
