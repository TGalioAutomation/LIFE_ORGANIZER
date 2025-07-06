from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.GoalCategoryViewSet, basename='goalcategory')
router.register(r'goals', views.GoalViewSet, basename='goal')
router.register(r'progress', views.GoalProgressViewSet, basename='goalprogress')
router.register(r'milestones', views.GoalMilestoneViewSet, basename='goalmilestone')
router.register(r'journal', views.JournalEntryViewSet, basename='journalentry')
router.register(r'reviews', views.MonthlyReviewViewSet, basename='monthlyreview')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', views.GoalAnalyticsView.as_view(), name='goal-analytics'),
    path('suggestions/', views.NextStepSuggestionsView.as_view(), name='next-step-suggestions'),
    path('habits/', views.HabitTrackingView.as_view(), name='habit-tracking'),
]
