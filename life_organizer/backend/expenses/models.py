from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class ExpenseCategory(models.Model):
    """Categories for organizing expenses"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon name/class
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_categories')

    # Predefined categories
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"
        unique_together = ['name', 'user']
        ordering = ['name']


class IncomeCategory(models.Model):
    """Categories for organizing income"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#28a745')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_categories')

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Income Category"
        verbose_name_plural = "Income Categories"
        unique_together = ['name', 'user']
        ordering = ['name']


class Transaction(models.Model):
    """Base model for all financial transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    # Categories
    expense_category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    income_category = models.ForeignKey(
        IncomeCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )

    # Date and time
    transaction_date = models.DateTimeField()

    # Optional fields
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    # Voice input metadata
    voice_input = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type.title()}: {self.amount} - {self.description}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-transaction_date']


class Budget(models.Model):
    """Monthly budgets for expense categories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='budgets')

    # Budget details
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    month = models.DateField()  # First day of the month

    # Alert settings
    alert_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('80.00'),
        help_text="Alert when spending reaches this percentage of budget"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def spent_amount(self):
        """Calculate total spent in this category for this month"""
        from django.db.models import Sum
        start_date = self.month
        end_date = start_date.replace(day=28) + models.timedelta(days=4)  # Next month
        end_date = end_date - models.timedelta(days=end_date.day)  # Last day of current month

        spent = Transaction.objects.filter(
            user=self.user,
            expense_category=self.category,
            transaction_type='expense',
            transaction_date__date__gte=start_date,
            transaction_date__date__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        return spent

    @property
    def remaining_amount(self):
        """Calculate remaining budget amount"""
        return self.amount - self.spent_amount

    @property
    def percentage_used(self):
        """Calculate percentage of budget used"""
        if self.amount == 0:
            return 0
        return (self.spent_amount / self.amount) * 100

    @property
    def is_over_budget(self):
        """Check if budget is exceeded"""
        return self.spent_amount > self.amount

    @property
    def should_alert(self):
        """Check if alert threshold is reached"""
        return self.percentage_used >= self.alert_threshold

    def __str__(self):
        return f"{self.category.name} Budget - {self.month.strftime('%B %Y')}: {self.amount}"

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ['user', 'category', 'month']
        ordering = ['-month', 'category__name']


class BudgetAlert(models.Model):
    """Alerts for budget thresholds"""
    ALERT_TYPES = [
        ('threshold', 'Threshold Reached'),
        ('exceeded', 'Budget Exceeded'),
        ('weekly_recap', 'Weekly Recap'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_alerts')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type.title()} Alert for {self.budget.category.name}"

    class Meta:
        verbose_name = "Budget Alert"
        verbose_name_plural = "Budget Alerts"
        ordering = ['-sent_at']
