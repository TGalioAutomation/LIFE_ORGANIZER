class ExpenseCategory {
  final int id;
  final String name;
  final String description;
  final String icon;
  final String color;
  final bool isDefault;
  final double totalSpent;
  final int transactionCount;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const ExpenseCategory({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    required this.color,
    required this.isDefault,
    required this.totalSpent,
    required this.transactionCount,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory ExpenseCategory.fromJson(Map<String, dynamic> json) {
    return ExpenseCategory(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String? ?? '',
      icon: json['icon'] as String? ?? '',
      color: json['color'] as String? ?? '#007bff',
      isDefault: json['is_default'] as bool? ?? false,
      totalSpent: (json['total_spent'] as num?)?.toDouble() ?? 0.0,
      transactionCount: json['transaction_count'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'icon': icon,
      'color': color,
      'is_default': isDefault,
      'total_spent': totalSpent,
      'transaction_count': transactionCount,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class IncomeCategory {
  final int id;
  final String name;
  final String description;
  final String icon;
  final String color;
  final bool isDefault;
  final double totalIncome;
  final int transactionCount;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const IncomeCategory({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    required this.color,
    required this.isDefault,
    required this.totalIncome,
    required this.transactionCount,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory IncomeCategory.fromJson(Map<String, dynamic> json) {
    return IncomeCategory(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String? ?? '',
      icon: json['icon'] as String? ?? '',
      color: json['color'] as String? ?? '#28a745',
      isDefault: json['is_default'] as bool? ?? false,
      totalIncome: (json['total_income'] as num?)?.toDouble() ?? 0.0,
      transactionCount: json['transaction_count'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'icon': icon,
      'color': color,
      'is_default': isDefault,
      'total_income': totalIncome,
      'transaction_count': transactionCount,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

enum TransactionType { income, expense }

class Transaction {
  final int id;
  final TransactionType transactionType;
  final double amount;
  final String description;
  final String notes;
  final int? expenseCategoryId;
  final int? incomeCategoryId;
  final String? categoryName;
  final String? categoryColor;
  final DateTime transactionDate;
  final String? receiptImage;
  final String? location;
  final bool voiceInput;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  const Transaction({
    required this.id,
    required this.transactionType,
    required this.amount,
    required this.description,
    required this.notes,
    this.expenseCategoryId,
    this.incomeCategoryId,
    this.categoryName,
    this.categoryColor,
    required this.transactionDate,
    this.receiptImage,
    this.location,
    required this.voiceInput,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory Transaction.fromJson(Map<String, dynamic> json) {
    return Transaction(
      id: json['id'] as int,
      transactionType: json['transaction_type'] == 'income' 
          ? TransactionType.income 
          : TransactionType.expense,
      amount: (json['amount'] as num).toDouble(),
      description: json['description'] as String,
      notes: json['notes'] as String? ?? '',
      expenseCategoryId: json['expense_category'] as int?,
      incomeCategoryId: json['income_category'] as int?,
      categoryName: json['category_name'] as String?,
      categoryColor: json['category_color'] as String?,
      transactionDate: DateTime.parse(json['transaction_date'] as String),
      receiptImage: json['receipt_image'] as String?,
      location: json['location'] as String?,
      voiceInput: json['voice_input'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'transaction_type': transactionType == TransactionType.income ? 'income' : 'expense',
      'amount': amount,
      'description': description,
      'notes': notes,
      'expense_category': expenseCategoryId,
      'income_category': incomeCategoryId,
      'category_name': categoryName,
      'category_color': categoryColor,
      'transaction_date': transactionDate.toIso8601String(),
      'receipt_image': receiptImage,
      'location': location,
      'voice_input': voiceInput,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
  
  bool get isIncome => transactionType == TransactionType.income;
  bool get isExpense => transactionType == TransactionType.expense;
}

class TransactionSummary {
  final double totalIncome;
  final double totalExpenses;
  final double netAmount;
  final int transactionCount;
  final String period;
  
  const TransactionSummary({
    required this.totalIncome,
    required this.totalExpenses,
    required this.netAmount,
    required this.transactionCount,
    required this.period,
  });
  
  factory TransactionSummary.fromJson(Map<String, dynamic> json) {
    return TransactionSummary(
      totalIncome: (json['total_income'] as num).toDouble(),
      totalExpenses: (json['total_expenses'] as num).toDouble(),
      netAmount: (json['net_amount'] as num).toDouble(),
      transactionCount: json['transaction_count'] as int,
      period: json['period'] as String,
    );
  }
}

class CategorySummary {
  final String categoryName;
  final String categoryColor;
  final double totalAmount;
  final int transactionCount;
  final double percentage;
  
  const CategorySummary({
    required this.categoryName,
    required this.categoryColor,
    required this.totalAmount,
    required this.transactionCount,
    required this.percentage,
  });
  
  factory CategorySummary.fromJson(Map<String, dynamic> json) {
    return CategorySummary(
      categoryName: json['category_name'] as String,
      categoryColor: json['category_color'] as String,
      totalAmount: (json['total_amount'] as num).toDouble(),
      transactionCount: json['transaction_count'] as int,
      percentage: (json['percentage'] as num).toDouble(),
    );
  }
}
