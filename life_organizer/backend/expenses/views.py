from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import calendar

from .models import ExpenseCategory, IncomeCategory, Transaction, Budget, BudgetAlert
from .serializers import (
    ExpenseCategorySerializer, IncomeCategorySerializer, TransactionSerializer,
    BudgetSerializer, BudgetAlertSerializer, TransactionSummarySerializer,
    CategorySummarySerializer, MonthlyTrendSerializer
)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing expense categories"""
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_defaults(self, request):
        """Create default expense categories for the user"""
        default_categories = [
            {'name': 'Food & Dining', 'icon': 'restaurant', 'color': '#FF5722'},
            {'name': 'Transportation', 'icon': 'directions_car', 'color': '#2196F3'},
            {'name': 'Shopping', 'icon': 'shopping_cart', 'color': '#9C27B0'},
            {'name': 'Entertainment', 'icon': 'movie', 'color': '#FF9800'},
            {'name': 'Bills & Utilities', 'icon': 'receipt', 'color': '#607D8B'},
            {'name': 'Healthcare', 'icon': 'local_hospital', 'color': '#4CAF50'},
            {'name': 'Education', 'icon': 'school', 'color': '#3F51B5'},
            {'name': 'Travel', 'icon': 'flight', 'color': '#00BCD4'},
        ]

        created_categories = []
        for cat_data in default_categories:
            category, created = ExpenseCategory.objects.get_or_create(
                user=request.user,
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_default': True
                }
            )
            if created:
                created_categories.append(category)

        serializer = self.get_serializer(created_categories, many=True)
        return Response({
            'message': f'Created {len(created_categories)} default categories',
            'categories': serializer.data
        })


class IncomeCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing income categories"""
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_defaults(self, request):
        """Create default income categories for the user"""
        default_categories = [
            {'name': 'Salary', 'icon': 'work', 'color': '#4CAF50'},
            {'name': 'Freelance', 'icon': 'laptop', 'color': '#2196F3'},
            {'name': 'Investment', 'icon': 'trending_up', 'color': '#FF9800'},
            {'name': 'Business', 'icon': 'business', 'color': '#9C27B0'},
            {'name': 'Other', 'icon': 'attach_money', 'color': '#607D8B'},
        ]

        created_categories = []
        for cat_data in default_categories:
            category, created = IncomeCategory.objects.get_or_create(
                user=request.user,
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_default': True
                }
            )
            if created:
                created_categories.append(category)

        serializer = self.get_serializer(created_categories, many=True)
        return Response({
            'message': f'Created {len(created_categories)} default categories',
            'categories': serializer.data
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['transaction_type', 'expense_category', 'income_category']
    search_fields = ['description', 'notes']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)

        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent transactions (last 10)"""
        transactions = self.get_queryset()[:10]
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary for a period"""
        queryset = self.get_queryset()

        # Calculate totals
        income_total = queryset.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = queryset.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        net_amount = income_total - expense_total
        transaction_count = queryset.count()

        # Determine period
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        period = 'custom'

        if not start_date and not end_date:
            period = 'all_time'
        elif start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            if (end - start).days <= 31:
                period = 'month'
            elif (end - start).days <= 7:
                period = 'week'

        summary_data = {
            'total_income': income_total,
            'total_expenses': expense_total,
            'net_amount': net_amount,
            'transaction_count': transaction_count,
            'period': period
        }

        serializer = TransactionSummarySerializer(summary_data)
        return Response(serializer.data)


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budgets"""
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['category', 'month']
    ordering = ['-month']

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """Get budgets for current month"""
        now = timezone.now()
        current_month = now.replace(day=1).date()

        budgets = self.get_queryset().filter(month=current_month)
        serializer = self.get_serializer(budgets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get budget alerts for current month"""
        now = timezone.now()
        current_month = now.replace(day=1).date()

        budgets = self.get_queryset().filter(month=current_month)
        alerts = []

        for budget in budgets:
            if budget.should_alert or budget.is_over_budget:
                alert_type = 'exceeded' if budget.is_over_budget else 'threshold'
                message = f"Budget for {budget.category.name} is "
                if budget.is_over_budget:
                    message += f"exceeded by ${budget.spent_amount - budget.amount:.2f}"
                else:
                    message += f"{budget.percentage_used:.1f}% used"

                alerts.append({
                    'budget_id': budget.id,
                    'category': budget.category.name,
                    'alert_type': alert_type,
                    'message': message,
                    'percentage_used': budget.percentage_used,
                    'is_over_budget': budget.is_over_budget
                })

        return Response(alerts)


class BudgetAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budget alerts"""
    serializer_class = BudgetAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['alert_type', 'is_read']
    ordering = ['-sent_at']

    def get_queryset(self):
        return BudgetAlert.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark alert as read"""
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response({'message': 'Alert marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all alerts as read"""
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All alerts marked as read'})


class ExpenseAnalyticsView(APIView):
    """Analytics for expenses"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Default to current month if no dates provided
        if not start_date or not end_date:
            now = timezone.now()
            start_date = now.replace(day=1).date()
            end_date = (start_date.replace(month=start_date.month + 1) - timedelta(days=1))
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Get transactions for the period
        transactions = Transaction.objects.filter(
            user=user,
            transaction_date__date__gte=start_date,
            transaction_date__date__lte=end_date
        )

        # Category-wise breakdown
        category_data = []
        expense_transactions = transactions.filter(transaction_type='expense')
        total_expenses = expense_transactions.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

        if total_expenses > 0:
            categories = expense_transactions.values(
                'expense_category__name',
                'expense_category__color'
            ).annotate(
                total_amount=Sum('amount'),
                transaction_count=Count('id')
            ).order_by('-total_amount')

            for cat in categories:
                percentage = (cat['total_amount'] / total_expenses) * 100
                category_data.append({
                    'category_name': cat['expense_category__name'],
                    'category_color': cat['expense_category__color'],
                    'total_amount': cat['total_amount'],
                    'transaction_count': cat['transaction_count'],
                    'percentage': percentage
                })

        # Monthly trends (last 6 months)
        monthly_trends = []
        for i in range(6):
            month_start = (timezone.now().replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start.replace(month=month_start.month + 1) - timedelta(days=1))

            month_transactions = Transaction.objects.filter(
                user=user,
                transaction_date__date__gte=month_start.date(),
                transaction_date__date__lte=month_end.date()
            )

            income = month_transactions.filter(
                transaction_type='income'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            expenses = month_transactions.filter(
                transaction_type='expense'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            monthly_trends.append({
                'month': month_start.strftime('%b %Y'),
                'income': income,
                'expenses': expenses,
                'net': income - expenses
            })

        monthly_trends.reverse()  # Show oldest to newest

        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'category_breakdown': CategorySummarySerializer(category_data, many=True).data,
            'monthly_trends': MonthlyTrendSerializer(monthly_trends, many=True).data,
            'total_expenses': total_expenses,
            'total_income': transactions.filter(
                transaction_type='income'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        })


class MonthlySummaryView(APIView):
    """Monthly summary of expenses and income"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get month and year from query params
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {'error': 'Invalid month or year'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate month start and end dates
        month_start = datetime(year, month, 1).date()
        month_end = datetime(year, month, calendar.monthrange(year, month)[1]).date()

        # Get transactions for the month
        transactions = Transaction.objects.filter(
            user=user,
            transaction_date__date__gte=month_start,
            transaction_date__date__lte=month_end
        )

        # Calculate totals
        income_total = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Get budgets for the month
        budgets = Budget.objects.filter(
            user=user,
            month=month_start
        )

        total_budget = budgets.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

        # Calculate daily averages
        days_in_month = calendar.monthrange(year, month)[1]
        daily_avg_income = income_total / days_in_month if income_total > 0 else Decimal('0.00')
        daily_avg_expense = expense_total / days_in_month if expense_total > 0 else Decimal('0.00')

        return Response({
            'month': calendar.month_name[month],
            'year': year,
            'total_income': income_total,
            'total_expenses': expense_total,
            'net_amount': income_total - expense_total,
            'total_budget': total_budget,
            'budget_remaining': total_budget - expense_total,
            'budget_used_percentage': (expense_total / total_budget * 100) if total_budget > 0 else 0,
            'daily_avg_income': daily_avg_income,
            'daily_avg_expense': daily_avg_expense,
            'transaction_count': transactions.count(),
            'days_in_month': days_in_month
        })
