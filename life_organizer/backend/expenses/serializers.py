from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal
from .models import ExpenseCategory, IncomeCategory, Transaction, Budget, BudgetAlert


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseCategory model"""
    total_spent = serializers.SerializerMethodField()
    transaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ExpenseCategory
        fields = [
            'id', 'name', 'description', 'icon', 'color', 'is_default',
            'total_spent', 'transaction_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_default', 'created_at', 'updated_at']
    
    def get_total_spent(self, obj):
        total = obj.transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')
    
    def get_transaction_count(self, obj):
        return obj.transactions.filter(transaction_type='expense').count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class IncomeCategorySerializer(serializers.ModelSerializer):
    """Serializer for IncomeCategory model"""
    total_income = serializers.SerializerMethodField()
    transaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = IncomeCategory
        fields = [
            'id', 'name', 'description', 'icon', 'color', 'is_default',
            'total_income', 'transaction_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_default', 'created_at', 'updated_at']
    
    def get_total_income(self, obj):
        total = obj.transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')
    
    def get_transaction_count(self, obj):
        return obj.transactions.filter(transaction_type='income').count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model"""
    category_name = serializers.SerializerMethodField()
    category_color = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'description', 'notes',
            'expense_category', 'income_category', 'category_name', 'category_color',
            'transaction_date', 'receipt_image', 'location', 'voice_input',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_category_name(self, obj):
        if obj.transaction_type == 'expense' and obj.expense_category:
            return obj.expense_category.name
        elif obj.transaction_type == 'income' and obj.income_category:
            return obj.income_category.name
        return None
    
    def get_category_color(self, obj):
        if obj.transaction_type == 'expense' and obj.expense_category:
            return obj.expense_category.color
        elif obj.transaction_type == 'income' and obj.income_category:
            return obj.income_category.color
        return None
    
    def validate(self, attrs):
        transaction_type = attrs.get('transaction_type')
        expense_category = attrs.get('expense_category')
        income_category = attrs.get('income_category')
        
        if transaction_type == 'expense':
            if not expense_category:
                raise serializers.ValidationError(
                    "Expense category is required for expense transactions"
                )
            if income_category:
                raise serializers.ValidationError(
                    "Income category should not be set for expense transactions"
                )
        elif transaction_type == 'income':
            if not income_category:
                raise serializers.ValidationError(
                    "Income category is required for income transactions"
                )
            if expense_category:
                raise serializers.ValidationError(
                    "Expense category should not be set for income transactions"
                )
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent_amount = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    percentage_used = serializers.ReadOnlyField()
    is_over_budget = serializers.ReadOnlyField()
    should_alert = serializers.ReadOnlyField()
    
    class Meta:
        model = Budget
        fields = [
            'id', 'category', 'category_name', 'amount', 'month',
            'alert_threshold', 'spent_amount', 'remaining_amount',
            'percentage_used', 'is_over_budget', 'should_alert',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_category(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError(
                "You can only create budgets for your own categories"
            )
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BudgetAlertSerializer(serializers.ModelSerializer):
    """Serializer for BudgetAlert model"""
    budget_category = serializers.CharField(source='budget.category.name', read_only=True)
    budget_amount = serializers.DecimalField(
        source='budget.amount', 
        max_digits=12, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = BudgetAlert
        fields = [
            'id', 'budget', 'budget_category', 'budget_amount',
            'alert_type', 'message', 'is_read', 'sent_at'
        ]
        read_only_fields = ['id', 'sent_at']


class TransactionSummarySerializer(serializers.Serializer):
    """Serializer for transaction summary data"""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    period = serializers.CharField()


class CategorySummarySerializer(serializers.Serializer):
    """Serializer for category-wise spending summary"""
    category_name = serializers.CharField()
    category_color = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class MonthlyTrendSerializer(serializers.Serializer):
    """Serializer for monthly spending trends"""
    month = serializers.CharField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net = serializers.DecimalField(max_digits=12, decimal_places=2)
