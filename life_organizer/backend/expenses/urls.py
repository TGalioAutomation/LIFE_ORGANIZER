from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.ExpenseCategoryViewSet, basename='expensecategory')
router.register(r'income-categories', views.IncomeCategoryViewSet, basename='incomecategory')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'budgets', views.BudgetViewSet, basename='budget')
router.register(r'alerts', views.BudgetAlertViewSet, basename='budgetalert')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', views.ExpenseAnalyticsView.as_view(), name='expense-analytics'),
    path('monthly-summary/', views.MonthlySummaryView.as_view(), name='monthly-summary'),
]
