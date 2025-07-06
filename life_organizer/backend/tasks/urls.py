from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'comments', views.TaskCommentViewSet, basename='taskcomment')
router.register(r'attachments', views.TaskAttachmentViewSet, basename='taskattachment')
router.register(r'reminders', views.TaskReminderViewSet, basename='taskreminder')
router.register(r'time-logs', views.TaskTimeLogViewSet, basename='tasktimelog')

urlpatterns = [
    path('', include(router.urls)),
    path('kanban/', views.KanbanBoardView.as_view(), name='kanban-board'),
    path('calendar/', views.TaskCalendarView.as_view(), name='task-calendar'),
    path('analytics/', views.TaskAnalyticsView.as_view(), name='task-analytics'),
]
